from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0.0"
)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    
tasks = [
    {"id": 1, "title": "Update to do list", "done": True},
    {"id": 2, "title": "Setup Flyrank profile", "done": True},
    {"id": 3, "title": "Go to the gym", "done": False},
]

@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get(
    "/tasks",
    summary="Get all tasks",
    description="Returns a list of all tasks."
)
async def show_tasks():
    return tasks

@app.get(
    "/tasks/{task_id}",
    summary="Get task by ID",
    description="Returns a single task if it exists."
)
async def get_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

# POST ENDPOINT
@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with the provided title."
)
async def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title, completion status, or both for an existing task."
)
async def update_task(task_id: int, updated: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            if updated.title is None and updated.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="Request body cannot be empty"
                )

            if updated.title is not None:
                if not updated.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = updated.title

            if updated.done is not None:
                task["done"] = updated.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )