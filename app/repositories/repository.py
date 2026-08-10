import os
import psycopg

from pathlib import Path
from dotenv import load_dotenv
from app.database.database import get_connection as get_sqlite_connection


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")


class TaskRepository:
    def __init__(self):
        self.initialize_postgres()

    def get_postgres_connection(self):
        return psycopg.connect(DATABASE_URL)

    def initialize_postgres(self):
        connection = self.get_postgres_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]

        if task_count == 0:
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                [
                    ("Update to do list", True),
                    ("Setup Flyrank profile", True),
                    ("Go to the gym", False),
                ]
            )

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(
        self,
        done: bool | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int = 0
    ):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        query = "SELECT id, title, done FROM tasks"
        conditions = []
        params = []

        if done is not None:
            conditions.append("done = ?")
            params.append(done)

        if search:
            conditions.append("title LIKE ?")
            params.append(f"%{search}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY title ASC"

        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.append(limit)
            params.append(offset)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        connection.close()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"])
            }
            for row in rows
        ]

    def get_by_id(self, task_id: int):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }

    def create(self, title: str):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title, False)
        )

        connection.commit()

        task_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()
        connection.close()

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }

    def update(
        self,
        task_id: int,
        title: str | None,
        done: bool | None
    ):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.fetchone() is None:
            connection.close()
            return None

        if title is not None:
            cursor.execute(
                "UPDATE tasks SET title = ? WHERE id = ?",
                (title, task_id)
            )

        if done is not None:
            cursor.execute(
                "UPDATE tasks SET done = ? WHERE id = ?",
                (done, task_id)
            )

        connection.commit()
        connection.close()

        return self.get_by_id(task_id)

    def delete(self, task_id: int):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted

    def get_stats(self):
        connection = get_sqlite_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
        done = cursor.fetchone()[0]

        connection.close()

        return {
            "total": total,
            "done": done,
            "open": total - done
        }