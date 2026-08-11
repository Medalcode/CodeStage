import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "studio.db"

def get_db_connection():
    """Retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa las tablas relacionales de la base de datos."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT,
                category TEXT,
                aspect_ratio TEXT DEFAULT '16:9',
                script_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_project(project_id: str, title: str, subtitle: str, category: str, script: Dict[str, Any], aspect_ratio: str = '16:9') -> Dict[str, Any]:
    """Guarda o actualiza un proyecto en la base de datos SQLite."""
    init_db()
    script_str = json.dumps(script, ensure_ascii=False)
    now = datetime.now(timezone.utc).isoformat()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (id, title, subtitle, category, aspect_ratio, script_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                subtitle=excluded.subtitle,
                category=excluded.category,
                aspect_ratio=excluded.aspect_ratio,
                script_json=excluded.script_json,
                updated_at=excluded.updated_at
        """, (project_id, title, subtitle, category, aspect_ratio, script_str, now, now))
        conn.commit()

    return get_project(project_id)

def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un proyecto por su ID."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "title": row["title"],
                "subtitle": row["subtitle"],
                "category": row["category"],
                "aspect_ratio": row["aspect_ratio"],
                "script": json.loads(row["script_json"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
    return None

def list_projects() -> List[Dict[str, Any]]:
    """Lista todos los proyectos guardados en la base de datos."""
    init_db()
    projects = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, subtitle, category, aspect_ratio, created_at FROM projects ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        for row in rows:
            projects.append({
                "id": row["id"],
                "title": row["title"],
                "subtitle": row["subtitle"],
                "category": row["category"],
                "aspect_ratio": row["aspect_ratio"],
                "created_at": row["created_at"],
            })
    return projects
