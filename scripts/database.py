from pathlib import Path
import sqlite3

# Project root (one level above /scripts)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Database path
DB_PATH = PROJECT_ROOT / "database" / "job_agent.db"


def get_connection():
    return sqlite3.connect(DB_PATH)