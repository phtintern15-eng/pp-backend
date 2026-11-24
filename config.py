"""
backend/config.py
MANDATORY — DB and environment configuration for cPanel/WSGI & Local Development.
Conforms strictly to Project Structure — Generalized Standard (cPanel-Oriented).
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Base paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
CSS_DIR = os.path.join(FRONTEND_DIR, "css")
JS_DIR = os.path.join(FRONTEND_DIR, "js")
IMAGES_DIR = os.path.join(FRONTEND_DIR, "images")
UPLOADS_DIR = os.path.join(FRONTEND_DIR, "uploads")
SQLITE_PATH = os.path.join(BACKEND_DIR, "primeproperty.db")

# Ensure required directories exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Load .env with encoding fallback (UTF-8 then latin-1 per cPanel spec)
env_path = os.path.join(BACKEND_DIR, ".env")
if os.path.exists(env_path):
    try:
        load_dotenv(env_path, encoding="utf-8")
    except Exception:
        try:
            load_dotenv(env_path, encoding="latin-1")
        except Exception:
            load_dotenv(env_path)
else:
    load_dotenv()


class Config:
    """Standardized environment and database configuration."""

    # Environment
    ENV = os.getenv("FLASK_ENV", os.getenv("ENV", "development"))
    DEBUG = os.getenv("DEBUG", "False" if ENV == "production" else "True").lower() in ("true", "1", "yes")

    # Security & Session Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "primeproperty-secret-key-production-change-in-env")
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

    # MySQL Database Settings (cPanel shared hosting optimized)
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "primeproperty_v2")
    DB_TYPE = os.getenv("DB_TYPE", "auto").lower()

    # Shared Host Connection Pooling (Safe for cPanel max_user_connections limits)
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "280"))
    DB_POOL_PRE_PING = True

    # Directories
    PROJECT_ROOT = PROJECT_ROOT
    BACKEND_DIR = BACKEND_DIR
    FRONTEND_DIR = FRONTEND_DIR
    CSS_DIR = CSS_DIR
    JS_DIR = JS_DIR
    IMAGES_DIR = IMAGES_DIR
    UPLOADS_DIR = UPLOADS_DIR
    SQLITE_PATH = SQLITE_PATH

    @classmethod
    def get_database_url(cls) -> str:
        url = os.getenv("DATABASE_URL")
        if url:
            return url
        if cls.DB_TYPE == "sqlite":
            return f"sqlite:///{cls.SQLITE_PATH}"
        return (
            f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@"
            f"{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}"
        )


config = Config()

