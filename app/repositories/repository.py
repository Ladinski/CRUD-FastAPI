class TaskRepository:
    def __init__(self):
        self.tasks = [
            {"id": 1, "title": "Update to do list", "done": True},
            {"id": 2, "title": "Setup Flyrank profile", "done": True},
            {"id": 3, "title": "Go to the gym", "done": False},
        ]

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                return task

        return None

    def create(self, title: str):
        new_id = max(
            (task["id"] for task in self.tasks),
            default=0
        ) + 1

        new_task = {
            "id": new_id,
            "title": title,
            "done": False
        }

        self.tasks.append(new_task)
        return new_task

    def update(
        self,
        task_id: int,
        title: str | None,
        done: bool | None
    ):
        task = self.get_by_id(task_id)

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