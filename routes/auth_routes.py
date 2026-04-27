from flask import Blueprint, request, render_template, redirect, url_for, make_response
import pyotp
import qrcode
import io
import base64
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from models.user_model import get_user_by_username, create_user
from utils.auth_utils import (
    hash_password, 
    verify_password, 
    generate_2fa_secret, 
    get_2fa_uri, 
    verify_2fa_token,
    generate_token
)

auth_bp = Blueprint("auth_bp", __name__)

# --- 1. التسجيل (Signup) ---
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("register.html")

    # القراءة من الـ Form لحل مشكلة 415
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "User")

    if not all([username, email, password]):
        return "خطأ: جميع الحقول مطلوبة", 400

    if get_user_by_username(username):
        return "خطأ: المستخدم موجود بالفعل", 409

    # تشفير البيانات وتوليد الـ 2FA
    pwd_hash = hash_password(password)
    two_fa_secret = generate_2fa_secret()
    
    if create_user(username, email, pwd_hash, role, two_fa_secret):
        # توليد كود الـ QR
        uri = get_2fa_uri(username, two_fa_secret)
        img = qrcode.make(uri)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()

        return render_template("setup_2fa.html", 
                               qr_code=qr_base64, 
                               secret=two_fa_secret, 
                               username=username)
    
    return "خطأ في إنشاء الحساب", 500

# --- 2. تسجيل الدخول (Login) ---
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username)
    if not user or not verify_password(user['password_hash'], password):
        return "خطأ: اسم المستخدم أو كلمة المرور غير صحيحة", 401

    # التوجه لصفحة الـ 2FA
    return render_template("verify_2fa.html", username=username)

# --- 3. التحقق من الـ 2FA وزرع التوكن (Verify 2FA & Set Token) ---
@auth_bp.route("/verify-2fa", methods=["POST"])
def verify_2fa():
    data = request.form
    username = data.get("username")
    otp_code = data.get("code")

    user = get_user_by_username(username)
    if not user:
        return "المستخدم غير موجود", 404

    # التحقق من كود Microsoft Authenticator
    if verify_2fa_token(user['two_fa_secret'], otp_code):
        # توليد التوكن (JWT)
        token = generate_token(user['id'], user['username'], user['email'], user['role'])
        
        # الحل النهائي: إرسال التوكن للمتصفح عبر الـ Cookies
        # هذا يسمح للمتصفح بالدخول للمسارات المحمية تلقائياً
        response = make_response(redirect(url_for('protected_bp.profile')))
        set_access_cookies(response, token)
        return response
    
    return "كود الـ 2FA غير صحيح" , 401

# --- 4. تسجيل الخروج (Logout) ---
@auth_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for('auth_bp.login')))
    unset_jwt_cookies(response) # مسح التوكن من المتصفح
    return response