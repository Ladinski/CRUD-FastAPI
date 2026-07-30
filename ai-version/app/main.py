from fastapi import FastAPI

from app.routers.router import router as tasks_router


app = FastAPI(
    title="Task Management API",
    description="A layered FastAPI REST API for managing in-memory tasks.",
    version="1.0.0",
)


@app.get(
    "/",
    summary="Get API information",
    description="Return basic information about the Task Management API.",
)
def get_api_info() -> dict[str, str]:
    return {
        "name": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get(
    "/health",
    summary="Health check",
    description="Return the current health status of the API.",
)
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(tasks_router)
