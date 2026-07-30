from app.schemas.schema import TaskResponse


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, TaskResponse] = {}
        self._next_id = 1

    def get_all(self) -> list[TaskResponse]:
        return list(self._tasks.values())

    def get_by_id(self, task_id: int) -> TaskResponse | None:
        return self._tasks.get(task_id)

    def create(self, title: str) -> TaskResponse:
        task = TaskResponse(id=self._next_id, title=title, done=False)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def update(self, task_id: int, update_data: dict[str, object]) -> TaskResponse | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        updated_task = task.model_copy(update=update_data)
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True
