from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.repositories.repository import TaskRepository
from app.schemas.schema import TaskCreate, TaskUpdate
from app.services.service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

repository = TaskRepository()
service = TaskService(repository)


@router.get(
    "",
    summary="Get all tasks",
    description="Returns tasks with optional filtering, searching, and pagination."
)
async def show_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0)
):
    return service.get_all_tasks(
        done=done,
        search=search,
        limit=limit,
        offset=offset
    )


@router.get(
    "/stats",
    summary="Task statistics",
    description="Returns the total, completed, and open task counts."
)
async def task_stats():
    return service.get_stats()


@router.get(
    "/{task_id}",
    summary="Get task by ID",
    description="Returns a single task if it exists."
)
async def get_task(task_id: int):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return task


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with the provided title."
)
async def create_task(task: TaskCreate):
    try:
        return service.create_task(task)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put(
    "/{task_id}",
    summary="Update a task",
    description="Updates the title, completion status, or both for an existing task."
)
async def update_task(task_id: int, updated: TaskUpdate):
    try:
        task = service.update_task(task_id, updated)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
async def delete_task(task_id: int):
    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )