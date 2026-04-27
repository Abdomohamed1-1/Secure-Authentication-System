import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # أضفنا قيم احتياطية (default values) عشان الـ RuntimeError يختفي تماماً
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-123")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secure-key-456")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 60))
    )
    
    DATABASE = os.getenv("DATABASE_NAME", "database.db")

    # إعدادات الكوكيز (دي اللي هتخليك تدخل الصفحات التانية)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_CSRF_PROTECT = False