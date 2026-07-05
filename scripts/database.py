import sqlite3
from pathlib import Path

# Find the project root automatically
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = PROJECT_ROOT / "database" / "ai_job_agent.db"


def get_connection():
    """Return a connection to the AI Job Agent database."""

    conn = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row

    return conn