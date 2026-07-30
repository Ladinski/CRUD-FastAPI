from app.repositories.repository import TaskRepository
from app.schemas.schema import TaskCreate, TaskResponse, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskValidationError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self._repository = repository or TaskRepository()

    def get_all_tasks(self) -> list[TaskResponse]:
        return self._repository.get_all()

    def get_task(self, task_id: int) -> TaskResponse:
        task = self._repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")
        return task

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        title = self._validate_title(task_data.title)
        return self._repository.create(title=title)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        existing_task = self._repository.get_by_id(task_id)
        if existing_task is None:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")

        update_data = task_data.model_dump(exclude_unset=True)
        if not update_data:
            raise TaskValidationError("At least one field must be provided.")

        if "title" in update_data:
            update_data["title"] = self._validate_title(update_data["title"])

        if "done" in update_data and update_data["done"] is None:
            raise TaskValidationError("Done must be true or false.")

        updated_task = self._repository.update(task_id, update_data)
        if updated_task is None:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")

        return updated_task

    def delete_task(self, task_id: int) -> None:
        deleted = self._repository.delete(task_id)
        if not deleted:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")

    @staticmethod
    def _validate_title(title: str | None) -> str:
        if title is None:
            raise TaskValidationError("Title must not be empty.")

        cleaned_title = title.strip()
        if not cleaned_title:
            raise TaskValidationError("Title must not be empty.")
        return cleaned_title
