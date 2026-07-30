from app.repositories.repository import TaskRepository
from app.schemas.schema import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all_tasks(
        self,
        done: bool | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int = 0
    ):
        return self.repository.get_all(
            done=done,
            search=search,
            limit=limit,
            offset=offset
        )

    def get_task(self, task_id: int):
        return self.repository.get_by_id(task_id)

    def get_stats(self):
        tasks = self.repository.get_all()

        total = len(tasks)
        done = sum(task["done"] for task in tasks)

        return {
            "total": total,
            "done": done,
            "open": total - done
        }
    
    def create_task(self, task: TaskCreate):
        if not task.title.strip():
            raise ValueError("Title cannot be empty")

        return self.repository.create(task.title)

    def update_task(self, task_id: int, updated: TaskUpdate):
        if updated.title is None and updated.done is None:
            raise ValueError("Request body cannot be empty")

        if updated.title is not None and not updated.title.strip():
            raise ValueError("Title cannot be empty")

        return self.repository.update(
            task_id,
            updated.title,
            updated.done
        )

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)