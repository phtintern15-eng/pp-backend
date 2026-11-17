"""
backend/export_db.py
Utility script to export MySQL database to:
1. documents/database.sql (MySQL dump)
2. backend/primeproperty.db (Portable SQLite database)
"""
import os
import sys
import subprocess
from sqlalchemy import create_engine, MetaData, select

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
DOCS_DIR = os.path.join(PROJECT_ROOT, "documents")
SQLITE_PATH = os.path.join(BACKEND_DIR, "primeproperty.db")
SQL_DUMP_PATH = os.path.join(DOCS_DIR, "database.sql")

sys.path.insert(0, BACKEND_DIR)
from config import config
from models import Base

def export_to_sqlite():
    print("[1/2] Exporting MySQL tables to portable SQLite (primeproperty.db)...")
    mysql_url = (
        f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@"
        f"{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}"
    )
    mysql_engine = create_engine(mysql_url)
    sqlite_engine = create_engine(f"sqlite:///{SQLITE_PATH}")

    # Recreate SQLite schema from models
    Base.metadata.drop_all(bind=sqlite_engine)
    Base.metadata.create_all(bind=sqlite_engine)

    ordered_tables = [
        'users',
        'clients',
        'consultant_profiles',
        'properties',
        'property_images',
        'consultations',
        'consultation_requests',
        'leads',
        'services',
        'service_requests',
        'user_sessions',
        'visitor_info'
    ]

    mysql_meta = MetaData()
    mysql_meta.reflect(bind=mysql_engine)

    with mysql_engine.connect() as m_conn, sqlite_engine.connect() as s_conn:
        for tbl_name in ordered_tables:
            if tbl_name in mysql_meta.tables and tbl_name in Base.metadata.tables:
                src_tbl = mysql_meta.tables[tbl_name]
                dst_tbl = Base.metadata.tables[tbl_name]
                rows = m_conn.execute(select(src_tbl)).fetchall()
                if rows:
                    insert_data = [dict(r._mapping) for r in rows]
                    s_conn.execute(dst_tbl.insert(), insert_data)
                    s_conn.commit()
                    print(f"  -> {tbl_name}: {len(rows)} rows synced")
                else:
                    print(f"  -> {tbl_name}: 0 rows (empty)")

    print(f"  [OK] Saved portable SQLite DB to: {SQLITE_PATH}")

def export_to_mysqldump():
    print("[2/2] Generating MySQL .sql dump...")
    mysqldump_candidates = [
        "mysqldump",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.1\bin\mysqldump.exe",
        r"C:\Program Files\MySQL\MySQL Workbench 8.0\mysqldump.exe",
        r"C:\xampp\mysql\bin\mysqldump.exe",
        r"C:\wamp64\bin\mysql\mysql8.0.31\bin\mysqldump.exe"
    ]
    dump_bin = None
    for candidate in mysqldump_candidates:
        try:
            res = subprocess.run([candidate, "--version"], capture_output=True, text=True)
            if res.returncode == 0:
                dump_bin = candidate
                break
        except Exception:
            continue

    if dump_bin:
        cmd = [
            dump_bin,
            f"-h{config.MYSQL_HOST}",
            f"-P{config.MYSQL_PORT}",
            f"-u{config.MYSQL_USER}",
            f"-p{config.MYSQL_PASSWORD}",
            "--routines",
            "--triggers",
            config.MYSQL_DB
        ]
        with open(SQL_DUMP_PATH, "w", encoding="utf-8") as out_file:
            res = subprocess.run(cmd, stdout=out_file, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                print(f"  [OK] Saved MySQL dump to: {SQL_DUMP_PATH}")
            else:
                print(f"  [!] mysqldump warning/error: {res.stderr}")
    else:
        print("  [!] mysqldump executable not found in PATH or standard directories.")

if __name__ == "__main__":
    try:
        export_to_sqlite()
        export_to_mysqldump()
        print("\nAll database files exported successfully! Ready for sharing.")
    except Exception as e:
        print(f"\n[ERROR] Export failed: {e}")

