from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

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

@app.get("/tasks")
async def show_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

# POST ENDPOINT
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

# PUT ENDPOINT

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            # Validate empty body
            if updated.title is None and updated.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="Request body cannot be empty"
                )

            # Update fields if provided
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


# DElETE ENDPOINT
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )