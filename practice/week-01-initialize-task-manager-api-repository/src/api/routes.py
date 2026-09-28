"""Task REST API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.task import (
    TaskCreate,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from src.services.task_service import TaskService, get_task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
    description="Create a new task with title, optional description, and status.",
)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Create a new task."""
    return service.create_task(task)


@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List Tasks",
    description="Retrieve all tasks, with optional filtering by status and search keyword.",
)
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(
        default=None,
        alias="status",
        description="Filter tasks by status (Pending, In Progress, Completed)",
    ),
    search: Optional[str] = Query(
        default=None,
        description="Search keyword matching title or description",
    ),
    service: TaskService = Depends(get_task_service),
) -> List[TaskResponse]:
    """List and filter tasks."""
    return service.list_tasks(status=status_filter, search=search)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Task by ID",
    description="Retrieve detailed information for a specific task by its identifier.",
)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Get single task by ID."""
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Task",
    description="Update title, description, or status of an existing task.",
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Update task fields."""
    updated = service.update_task(task_id, task_update)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return updated


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
    description="Remove a task permanently by its ID.",
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete task by ID."""
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return None
