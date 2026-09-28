"""Task domain models and Pydantic schemas."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    """Enumeration of allowed task lifecycle statuses."""

    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class TaskBase(BaseModel):
    """Base schema attributes shared by task inputs and outputs."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Concise title for the task (1-200 characters)",
        examples=["Complete project scaffolding"]
    )
    description: Optional[str] = Field(
        default="",
        max_length=1000,
        description="Detailed description or context for the task",
        examples=["Initialize directories, FastAPI routes, and automated tests"]
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current progress state of the task",
        examples=[TaskStatus.PENDING]
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task; all fields are optional."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated title of the task",
        examples=["Updated project scaffolding"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated description of the task",
        examples=["Updated details for scaffolding"]
    )
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Updated status of the task",
        examples=[TaskStatus.COMPLETED]
    )


class TaskResponse(TaskBase):
    """Schema returned to clients representing a persisted task."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique auto-incremented task ID", examples=[1])
    created_at: datetime = Field(..., description="UTC timestamp of creation")
    updated_at: datetime = Field(..., description="UTC timestamp of last update")
