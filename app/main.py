from fastapi import FastAPI
from app.routers.router import router as task_router
from app.database.database import initialize_database
from app.auth.supabase_client import supabase
from app.routers.auth_router import router as auth_router
from app.routers.protected_router import router as protected_router
from app.routers.llm_router import router as llm_router

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0.0"
)

print("Server running and connected to Supabase")

initialize_database()

app.include_router(task_router)
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(llm_router)

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