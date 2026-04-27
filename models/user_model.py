from db import get_connection

# --- 1. دوال جلب البيانات (Read Operations) ---

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    # يفضل تحديد الأعمدة بالاسم بدلاً من * لتجنب أخطاء الهيكل
    user = cursor.execute(
        "SELECT id, username, email, password_hash, role, two_fa_secret FROM users WHERE username = ?", 
        (username,)
    ).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    """البحث عن مستخدم بواسطة البريد الإلكتروني"""
    conn = get_connection()
    cursor = conn.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """البحث عن مستخدم بواسطة المعرف الفريد (ID)"""
    conn = get_connection()
    cursor = conn.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user

# --- 2. دوال إنشاء البيانات (Write Operations) ---

def create_user(username, email, password_hash, role, two_fa_secret):
    """
    إضافة مستخدم جديد لقاعدة البيانات.
    لاحظ أننا نخزن الـ password_hash وليس كلمة المرور الأصلية[cite: 1, 24].
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role, two_fa_secret)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, role, two_fa_secret)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ خطأ أثناء إنشاء المستخدم: {e}")
        return False