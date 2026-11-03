
import sqlite3
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "rewear.db"

# Create database directory automatically
DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Create a connection to the ReWear database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all database tables."""

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS clothing (
                clothing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                colour TEXT,
                occasion TEXT,
                season TEXT,
                image_path TEXT,
                wear_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS outfits (
                outfit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                outfit_name TEXT NOT NULL,
                occasion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS outfit_items (
                outfit_id INTEGER NOT NULL,
                clothing_id INTEGER NOT NULL,
                PRIMARY KEY (outfit_id, clothing_id),
                FOREIGN KEY (outfit_id)
                    REFERENCES outfits(outfit_id) ON DELETE CASCADE,
                FOREIGN KEY (clothing_id)
                    REFERENCES clothing(clothing_id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS wear_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                outfit_id INTEGER,
                clothing_id INTEGER,
                worn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (outfit_id)
                    REFERENCES outfits(outfit_id) ON DELETE SET NULL,
                FOREIGN KEY (clothing_id)
                    REFERENCES clothing(clothing_id) ON DELETE SET NULL
            )
        """)

    print("ReWear database initialized successfully!")


def get_dashboard_stats():
    """Retrieve real statistics for the dashboard."""

    with get_connection() as conn:

        total_clothes = conn.execute(
            "SELECT COUNT(*) FROM clothing"
        ).fetchone()[0]

        total_outfits = conn.execute(
            "SELECT COUNT(*) FROM outfits"
        ).fetchone()[0]

        total_worn = conn.execute(
            "SELECT COUNT(*) FROM wear_history"
        ).fetchone()[0]

        favourite = conn.execute("""
            SELECT category, COUNT(*) AS total
            FROM clothing
            GROUP BY category
            ORDER BY total DESC, category ASC
            LIMIT 1
        """).fetchone()

        return {
            "total_clothes": total_clothes,
            "total_outfits": total_outfits,
            "total_worn": total_worn,
            "favourite_category": (
                favourite["category"] if favourite else "None yet"
            )
        }


def get_recent_clothes(limit=5):
    """Retrieve recently added clothing."""

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT *
            FROM clothing
            ORDER BY created_at DESC, clothing_id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    print(get_dashboard_stats())
