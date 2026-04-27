from flask import Blueprint, jsonify, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user_model import get_user_by_id

protected_bp = Blueprint("protected_bp", __name__)

# --- 1. صفحة الملف الشخصي (Profile) ---
@protected_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if not user:
        return "المستخدم غير موجود", 404

    # عرض صفحة HTML بدلاً من JSON للمتصفح
    return render_template("profile.html", 
                           username=user['username'], 
                           email=user['email'], 
                           role=user['role'])

# --- 2. منطقة الـ User العادي ---
@protected_bp.route("/user-area", methods=["GET"])
@jwt_required()
def user_area():
    claims = get_jwt()
    if claims.get("role") not in ["User", "Manager", "Admin"]:
        return "غير مصرح لك بالدخول", 403
    
    return render_template("user_page.html", username=claims.get("username"))

# --- 3. منطقة الـ Manager (مطلوب في التكليف) ---
@protected_bp.route("/manager-area", methods=["GET"])
@jwt_required()
def manager_area():
    claims = get_jwt()
    # التحقق من الصلاحيات (المدير والأدمن فقط)
    if claims.get("role") not in ["Manager", "Admin"]:
        return "هذه المنطقة للمديرين فقط", 403

    return render_template("manager_page.html", username=claims.get("username"))

# --- 4. منطقة الـ Admin (مطلوب في التكليف) ---
@protected_bp.route("/admin-area", methods=["GET"])
@jwt_required()
def admin_area():
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return "وصول مرفوض: للأدمن فقط", 403

    return render_template("admin_page.html", username=claims.get("username"))