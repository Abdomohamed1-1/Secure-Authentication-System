import sqlite3
from flask import current_app

def get_connection():
    """
    إنشاء اتصال آمن ومنظم بقاعدة بيانات SQLite الخارجية.
    """
    try:
        # جلب مسار قاعدة البيانات من ملف الـ Config
        db_path = current_app.config.get('DATABASE', 'database.db')
        
        # إنشاء الاتصال
        conn = sqlite3.connect(db_path)
        
        # 1. تمكين الوصول للبيانات بأسماء الأعمدة (Dictionary-like access)
        # ده بيخليك تستخدم user['username'] بدل user[1] في الكود
        conn.row_factory = sqlite3.Row 
        
        # 2. تفعيل قيود المفاتيح الخارجية (Foreign Key Constraints)
        # خطوة مهمة جداً لضمان "Data Integrity" في قواعد البيانات
        conn.execute("PRAGMA foreign_keys = ON;")
        
        return conn
        
    except sqlite3.Error as e:
        print(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return None