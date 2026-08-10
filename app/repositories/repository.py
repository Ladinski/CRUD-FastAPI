from app.database.database import get_connection


class TaskRepository:
    def __init__(self):
        self.tasks = [
            {"id": 1, "title": "Update to do list", "done": True},
            {"id": 2, "title": "Setup Flyrank profile", "done": True},
            {"id": 3, "title": "Go to the gym", "done": False},
        ]

    def get_all(
        self,
        done: bool | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int = 0
    ):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, done FROM tasks"
        )

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
        connection = get_connection()
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
        connection = get_connection()
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
        task = None

        for existing_task in self.tasks:
            if existing_task["id"] == task_id:
                task = existing_task
                break

        if task is None:
            return None

        if title is not None:
            task["title"] = title

        if done is not None:
            task["done"] = done

        return task

    def delete(self, task_id: int):
        for index, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(index)
                return True

        return False