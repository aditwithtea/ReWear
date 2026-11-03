
import shutil
from pathlib import Path

from backend.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def add_clothing(name, category, colour, occasion, season, image_path):

    if not name.strip():
        raise ValueError("Clothing name is required.")

    saved_image = None

    # Copy uploaded image into project uploads folder
    if image_path:
        source = Path(image_path)

        if not source.exists():
            raise ValueError("Selected image does not exist.")

        allowed = {".jpg", ".jpeg", ".png", ".webp"}

        if source.suffix.lower() not in allowed:
            raise ValueError("Please select JPG, PNG or WEBP.")

        destination = UPLOAD_DIR / (
            f"clothing_{__import__('uuid').uuid4().hex}"
            f"{source.suffix.lower()}"
        )

        shutil.copy2(source, destination)

        saved_image = destination.relative_to(BASE_DIR).as_posix()

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO clothing
            (name, category, colour, occasion, season, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name.strip(),
            category,
            colour,
            occasion,
            season,
            saved_image
        ))

        return cursor.lastrowid


def get_all_clothing(search="", category="All", colour="All"):

    query = "SELECT * FROM clothing WHERE 1=1"
    params = []

    if search.strip():
        query += " AND name LIKE ?"
        params.append(f"%{search.strip()}%")

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    if colour != "All":
        query += " AND colour = ?"
        params.append(colour)

    query += " ORDER BY created_at DESC, clothing_id DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def delete_clothing(clothing_id):

    with get_connection() as conn:

        row = conn.execute(
            "SELECT image_path FROM clothing WHERE clothing_id = ?",
            (clothing_id,)
        ).fetchone()

        if row is None:
            return False

        conn.execute(
            "DELETE FROM clothing WHERE clothing_id = ?",
            (clothing_id,)
        )

        return True
