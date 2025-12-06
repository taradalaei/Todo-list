from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Optional

from app.models.task import MAX_DESC_LEN, MAX_TITLE_LEN, Task
from app.exceptions.base import ValidationError, NotFoundError


@dataclass(slots=True)
class Project:
    """Container for a collection of tasks."""

    id: int
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("project name cannot be empty")
        if len(self.name) > MAX_TITLE_LEN:
            raise ValidationError(
                f"project name must be maximum {MAX_TITLE_LEN} characters"
            )
        if len(self.description) > MAX_DESC_LEN:
            raise ValidationError(
                f"project description must be maximum {MAX_DESC_LEN} characters"
            )

    # --- Task management ----------------------------------------------
    def add_task(self, task: Task) -> None:
        """Append a task to this project."""
        # 1️⃣ Check duplicate ID
        if any(t.id == task.id for t in self.tasks):
            raise ValidationError(f"task id {task.id} already exists in project")
        
        # 2️⃣ Check duplicate title
        if any(t.title.strip().lower() == task.title.strip().lower() for t in self.tasks):
            raise ValidationError(f"task title '{task.title}' already exists in this project")


        # 3️⃣ Validate deadline if provided
        if task.deadline:
            try:
                deadline_dt = datetime.strptime(task.deadline, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    f"Deadline '{task.deadline}' is invalid. Use YYYY-MM-DD format."
                )

            # 4️⃣ Check if deadline is in the past
            if deadline_dt.date() < datetime.now().date():
                raise ValidationError("Deadline cannot be in the past.")

            # Optional: if you have a project start date
            if hasattr(self, 'start_date') and deadline_dt.date() < self.start_date:
                raise ValidationError("Deadline cannot be before project start date.")

            ## Store the parsed datetime if you want consistent type
            #task.deadline = deadline_dt

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
            if not name.strip():
                raise ValidationError("project name cannot be empty")
            
            if len(name) > MAX_TITLE_LEN:
                raise ValidationError(
                    f"project name must be maximum {MAX_TITLE_LEN} characters"
                )
            self.name = name
        if description is not None:
            if len(description) > MAX_DESC_LEN:
                raise ValidationError(
                    f"project description must be maximum {MAX_DESC_LEN} characters"
                )
            self.description = description

    # --- Query helpers -------------------------------------------------
    def list_tasks(self) -> list[Task]:
        return list(self.tasks)

    def iter_tasks(self) -> Iterable[Task]:
        return iter(self.tasks)
