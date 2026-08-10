from fastapi import FastAPI
from app.routers.router import router as task_router
from app.database.database import initialize_database

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0.0"
)

initialize_database()

app.include_router(task_router)


@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}