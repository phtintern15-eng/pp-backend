"""
backend/config.py
DB and environment configuration for cPanel/WSGI & Local Development.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BACKEND_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()


class Config:
    """Standardized environment and database configuration."""

    # Base paths & Directories
    BACKEND_DIR = BACKEND_DIR
    PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
    FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
    CSS_DIR = os.path.join(FRONTEND_DIR, "css")
    JS_DIR = os.path.join(FRONTEND_DIR, "js")
    IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")
    UPLOADS_DIR = os.path.join(FRONTEND_DIR, "uploads")
    SQL_FILE_PATH = os.path.join(BACKEND_DIR, "primeproperty.sql")

    # Environment
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False" if ENV == "production" else "True").lower() in ("true", "1", "yes")

    # Security & Session Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "primeproperty-ultra-luxury-secret-key-2026")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "prime_session")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in ("true", "1", "yes")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Proxy & Hosting (cPanel Apache/LiteSpeed)
    BEHIND_PROXY = os.getenv("BEHIND_PROXY", "false").lower() in ("true", "1", "yes")
    PUBLIC_DOMAIN = os.getenv("PUBLIC_DOMAIN", "localhost:8000")

    # Database URL (Loaded directly from .env)
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/primeproperty_v2")

    @classmethod
    def get_database_url(cls) -> str:
        return cls.DATABASE_URL


config = Config()
