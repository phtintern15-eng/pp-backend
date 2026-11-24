"""
backend/database.py
SQLAlchemy Database Engine and Session Factory.
Supports MySQL with connection pooling optimized for cPanel shared hosting,
with automatic SQLite fallback for local development.
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure backend dir is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import config

DATABASE_URL = config.get_database_url()
sqlite_path = config.SQLITE_PATH

engine = None

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    print("  [*] Database: Connected to local SQLite (primeproperty.db)")
else:
    try:
        # Optimized for cPanel shared hosting (Rule 2: Database)
        engine = create_engine(
            DATABASE_URL,
            pool_size=config.DB_POOL_SIZE,
            max_overflow=config.DB_MAX_OVERFLOW,
            pool_recycle=config.DB_POOL_RECYCLE,
            pool_pre_ping=config.DB_POOL_PRE_PING,
            echo=False,
            connect_args={"charset": "utf8mb4"}
        )
        # Test connection immediately
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"  [*] Database: Connected to MySQL ({config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB})")
    except Exception as e:
        print(f"  [!] Note: MySQL not available ({e}). Falling back to SQLite.")
        DATABASE_URL = f"sqlite:///{sqlite_path}"
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
        print("  [*] Database: Running with local SQLite fallback")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database session generator for Flask request lifecycle
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
