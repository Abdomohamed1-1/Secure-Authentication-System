import pyotp
import qrcode
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

# تهيئة Bcrypt لتشفير كلمات المرور (Password Hashing)
bcrypt = Bcrypt()

# --- 1. التعامل مع كلمات المرور (Password Security) ---

def hash_password(password):
    """تشفير كلمة المرور قبل تخزينها في قاعدة البيانات [cite: 22, 23, 24]"""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(hashed_password, plain_password):
    """مقارنة كلمة المرور المدخلة بالهاش المخزن عند تسجيل الدخول [cite: 25]"""
    return bcrypt.check_password_hash(hashed_password, plain_password)


# --- 2. إعداد الـ 2FA (Microsoft/Google Authenticator) ---

def generate_2fa_secret():
    """توليد مفتاح سري فريد (Secret Key) لكل مستخدم [cite: 40, 96]"""
    return pyotp.random_base32()

def get_2fa_uri(username, secret):
    """توليد الرابط القياسي الذي تقرأه تطبيقات Microsoft و Google Authenticator [cite: 42]"""
    # 'SecureAuthSystem' هو اسم المشروع الذي سيظهر داخل التطبيق للمستخدم
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=username, 
        issuer_name="SecureAuthSystem"
    )

def verify_2fa_token(secret, token):
    """التحقق من الكود المكون من 6 أرقام الذي يدخله المستخدم [cite: 43, 101]"""
    totp = pyotp.totp.TOTP(secret)
    return totp.verify(token)


# --- 3. إدارة التوكن (JWT Token Management) ---

def generate_token(user_id, username, email, role):
    """
    توليد توكن (JWT) بعد نجاح تسجيل الدخول والـ 2FA [cite: 48, 102]
    يحتوي التوكن على الـ Role للتحكم في الصلاحيات لاحقاً [cite: 104]
    """
    additional_claims = {
        "username": username,
        "email": email,
        "role": role  # ضروري لتنفيذ الـ RBAC المطلوب [cite: 66, 67]
    }
    # صلاحية التوكن ساعة واحدة مثلاً
    return create_access_token(identity=str(user_id), additional_claims=additional_claims, expires_delta=timedelta(hours=1))