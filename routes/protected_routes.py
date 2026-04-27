from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

protected_bp = Blueprint("protected_bp", __name__)

# --- Helper Function للتحقق من الأدوار ---
def check_role(required_role):
    claims = get_jwt()
    user_role = claims.get("role")
    if user_role != required_role:
        return False
    return True

# --- 1. مسار الـ Admin فقط ---
@protected_bp.route("/admin-area", methods=["GET"])
@jwt_required()
def admin_area():
    if not check_role("Admin"):
        return jsonify({"message": "Access denied: Admins only"}), 403
    
    return jsonify({
        "message": "Welcome to the Admin Dashboard",
        "access_level": "High"
    }), 200

# --- 2. مسار الـ Manager فقط ---
@protected_bp.route("/manager-area", methods=["GET"])
@jwt_required()
def manager_area():
    if not check_role("Manager"):
        return jsonify({"message": "Access denied: Managers only"}), 403
    
    return jsonify({
        "message": "Welcome to the Managerial Panel",
        "access_level": "Medium"
    }), 200

# --- 3. مسار الـ User العادي ---
@protected_bp.route("/user-area", methods=["GET"])
@jwt_required()
def user_area():
    # أي مستخدم مسجل (بما في ذلك Admin و Manager) يمكنه دخول منطقة المستخدمين
    # لكن لو أردت حصرها على دور 'User' فقط، استخدم check_role("User")
    return jsonify({
        "message": "Welcome to the User Profile area",
        "access_level": "Standard"
    }), 200

# --- 4. مسار عام للملف الشخصي (Profile) ---
@protected_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    claims = get_jwt()
    return jsonify({
        "username": claims.get("username"),
        "email": claims.get("email"),
        "role": claims.get("role")
    }), 200