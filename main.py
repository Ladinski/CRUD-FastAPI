from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Update to do list", "done": True},
    {"id": 2, "title": "Setup Flyrank profile", "done": True},
    {"id": 3, "title": "Go to the gym", "done": False},
]

@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def status():
    return {"status": "ok"}

@app.get("/tasks")
async def status():
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