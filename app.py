from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth_bp
from routes.protected_bp import protected_bp # تأكد من الاسم الصحيح للملف
from utils.auth_utils import bcrypt
import os

app = Flask(__name__)

# 1. تحميل الإعدادات من ملف config.py
# تأكد أن ملف config.py يحتوي على JWT_TOKEN_LOCATION = ['cookies']
app.config.from_object(Config)

# 2. إعداد الملحقات (Extensions)
bcrypt.init_app(app)
jwt = JWTManager(app)

# 3. تسجيل الـ Blueprints
# تم حذف الـ url_prefix أو تعديله ليتناسب مع الروابط في ملفات HTML
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(protected_bp) # المسارات المحمية تبدأ مباشرة بـ /profile أو /admin-area

# 4. التأكد من وجود المجلدات الضرورية للـ CSS والـ Database
if not os.path.exists('static'):
    os.makedirs('static')

# --- المسارات الرئيسية (Main Routes) ---

@app.route('/')
def index():
    """توجيه المستخدم لصفحة تسجيل الدخول عند فتح الموقع"""
    return redirect(url_for('auth_bp.login'))

# معالجة أخطاء JWT لضمان عدم ظهور رسائل JSON مزعجة للمستخدم
@jwt.unauthorized_loader
def unauthorized_response(callback):
    """إذا حاول المستخدم دخول صفحة محمية بدون تسجيل دخول"""
    return redirect(url_for('auth_bp.login'))

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    """إذا انتهت صلاحية التوكن (السيشن)"""
    return redirect(url_for('auth_bp.login'))

if __name__ == "__main__":
    # التأكد من أن قاعدة البيانات منشأة
    if not os.path.exists(app.config.get('DATABASE', 'database.db')):
        print("⚠️ قاعدة البيانات غير موجودة! يرجى تشغيل init_db.py أولاً.")
    
    app.run(debug=True, port=5000)