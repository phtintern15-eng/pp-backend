"""
backend/database.py
SQLAlchemy Database Engine and Session Factory.
Supports MySQL with connection pooling optimized for cPanel shared hosting and local MySQL,
without writing .db files to the backend folder.
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

def build_mysql_engine(url):
    """Build a MySQL engine with standard connection pooling."""
    return create_engine(
        url,
        pool_size=10,
        max_overflow=20,
        pool_recycle=280,
        pool_pre_ping=True,
        echo=False,
        connect_args={"charset": "utf8mb4"}
    )

engine = None

if DATABASE_URL.startswith("sqlite"):
    # If explicitly configured for SQLite, use in-memory to prevent creating .db files in backend/
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    print("  [*] Database: Connected to in-memory SQLite")
else:
    # 1. Attempt connection using primary configured URL (.env)
    target_display = DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL
    try:
        candidate_engine = build_mysql_engine(DATABASE_URL)
        with candidate_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = candidate_engine
        print(f"  [*] Database: Connected to MySQL ({target_display})")
    except Exception as primary_err:
        print(f"  [!] Note: Primary MySQL ({target_display}) connection failed: {primary_err}")

        # 2. If primary failed (e.g. remote host blocking client IP), attempt local MySQL
        connected_local = False
        local_candidates = [
            "mysql+pymysql://root:root@localhost:3306/primeproperty_v2",
            "mysql+pymysql://root:root@localhost:3306/primeproperty"
        ]
        for local_url in local_candidates:
            try:
                candidate_engine = build_mysql_engine(local_url)
                with candidate_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                engine = candidate_engine
                connected_local = True
                db_name = local_url.split("/")[-1]
                print(f"  [*] Database: Connected to local MySQL (localhost:3306/{db_name})")
                break
            except Exception:
                continue

        # 3. If no MySQL server reachable, fall back to in-memory SQLite (zero disk footprint)
        if not connected_local:
            print("  [!] Warning: No MySQL database reachable. Using in-memory fallback (no .db file created).")
            engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

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
