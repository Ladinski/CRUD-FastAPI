from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.schema import TaskCreate, TaskResponse, TaskUpdate
from app.services.service import TaskNotFoundError, TaskService, TaskValidationError


router = APIRouter(prefix="/tasks", tags=["tasks"])
task_service = TaskService()


@router.get(
    "",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description="Return all tasks currently stored in memory.",
)
def get_tasks() -> list[TaskResponse]:
    return task_service.get_all_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task",
    description="Return a single task by its integer ID.",
)
def get_task(task_id: int) -> TaskResponse:
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
    description="Create a new task with done defaulting to false.",
)
def create_task(task_data: TaskCreate) -> TaskResponse:
    try:
        return task_service.create_task(task_data)
    except TaskValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Partially update an existing task title, done state, or both.",
)
def update_task(task_id: int, task_data: TaskUpdate) -> TaskResponse:
    try:
        return task_service.update_task(task_id, task_data)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except TaskValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete an existing task by its integer ID.",
)
def delete_task(task_id: int) -> Response:
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
