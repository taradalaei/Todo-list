from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Optional

from .exceptions import NotFoundError, ValidationError
from .task import MIN_DESC_LEN, MIN_TITLE_LEN, Task

@dataclass(slots=True)
class Project:
    """Container for a collection of tasks."""

    id: int
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.name) < MIN_TITLE_LEN:
            raise ValidationError(
                f"project name must be at least {MIN_TITLE_LEN} characters"
            )
        if len(self.description) < MIN_DESC_LEN:
            raise ValidationError(
                f"project description must be at least {MIN_DESC_LEN} characters"
            )

    # --- Task management ----------------------------------------------
    def add_task(self, task: Task) -> None:
        """Append a task to this project."""
        if any(t.id == task.id for t in self.tasks):
            raise ValidationError(f"task id {task.id} already exists in project")
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove task by id, raise if not present."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) == before:
            raise NotFoundError(f"task {task_id} not found in project {self.id}")

    def get_task(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise NotFoundError(f"task {task_id} not found in project {self.id}")

    # --- Editing -------------------------------------------------------
    def rename(self, *, name: Optional[str] = None, description: Optional[str] = None) -> None:
        if name is not None:
            if len(name) < MIN_TITLE_LEN:
                raise ValidationError(
                    f"project name must be at least {MIN_TITLE_LEN} characters"
                )
            self.name = name
        if description is not None:
            if len(description) < MIN_DESC_LEN:
                raise ValidationError(
                    f"project description must be at least {MIN_DESC_LEN} characters"
                )
            self.description = description

    # --- Query helpers -------------------------------------------------
    def list_tasks(self) -> list[Task]:
        return list(self.tasks)

    def iter_tasks(self) -> Iterable[Task]:
        return iter(self.tasks)
