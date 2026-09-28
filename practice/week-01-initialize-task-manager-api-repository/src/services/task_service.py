"""Task business logic and in-memory persistence layer."""
from datetime import datetime, timezone
import threading
from typing import Dict, List, Optional

from src.models.task import (
    TaskCreate,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


class TaskService:
    """Thread-safe service managing Task CRUD operations and state transitions."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tasks: Dict[int, TaskResponse] = {}
        self._next_id: int = 1

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task and assign an auto-incrementing ID."""
        with self._lock:
            task_id = self._next_id
            self._next_id += 1

            now = datetime.now(timezone.utc)
            task = TaskResponse(
                id=task_id,
                title=task_data.title,
                description=task_data.description or "",
                status=task_data.status,
                created_at=now,
                updated_at=now,
            )
            self._tasks[task_id] = task
            return task

    def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """Retrieve a task by its unique ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        search: Optional[str] = None,
    ) -> List[TaskResponse]:
        """List tasks with optional filtering by status and title search keyword."""
        with self._lock:
            tasks = list(self._tasks.values())

        if status is not None:
            tasks = [t for t in tasks if t.status == status]

        if search:
            query = search.strip().lower()
            tasks = [
                t for t in tasks
                if query in t.title.lower() or (t.description and query in t.description.lower())
            ]

        return sorted(tasks, key=lambda t: t.id)

    def update_task(self, task_id: int, update_data: TaskUpdate) -> Optional[TaskResponse]:
        """Update fields of an existing task."""
        with self._lock:
            existing = self._tasks.get(task_id)
            if existing is None:
                return None

            now = datetime.now(timezone.utc)
            updated_title = update_data.title if update_data.title is not None else existing.title
            updated_description = (
                update_data.description if update_data.description is not None else existing.description
            )
            updated_status = update_data.status if update_data.status is not None else existing.status

            updated_task = TaskResponse(
                id=existing.id,
                title=updated_title,
                description=updated_description,
                status=updated_status,
                created_at=existing.created_at,
                updated_at=now,
            )
            self._tasks[task_id] = updated_task
            return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def clear(self) -> None:
        """Clear all tasks; useful for resetting state in test suites."""
        with self._lock:
            self._tasks.clear()
            self._next_id = 1


# Global singleton instance for service injection
_task_service_instance: Optional[TaskService] = None


def get_task_service() -> TaskService:
    """Dependency provider for TaskService."""
    global _task_service_instance
    if _task_service_instance is None:
        _task_service_instance = TaskService()
    return _task_service_instance
