
from __future__ import annotations
from datetime import date

import os
from typing import Optional

from dotenv import load_dotenv

from app.models.project import Project
from app.models.task import Task
from app.exceptions.base import ValidationError, NotFoundError


load_dotenv()  # Load environment variables

PROJECT_MAX = int(os.getenv("PROJECT_OF_NUMBER_MAX", "5"))
TASK_MAX = int(os.getenv("TASK_OF_NUMBER_MAX", "20"))


class InMemoryStorage:
    """Simple in-memory storage for projects and tasks."""

    def __init__(self) -> None:
        self.projects: dict[int, Project] = {}
        self._project_counter = 1
        self._task_counter = 1

    # --- Project operations --------------------------------------------
    def add_project(self, name: str, description: str) -> Project:
        """Add a new project if name unique and limit not exceeded."""
        if len(self.projects) >= PROJECT_MAX:
            raise ValidationError("maximum number of projects reached")

        if any(p.name == name for p in self.projects.values()):
            raise ValidationError(f"project name '{name}' already exists")

        project = Project(self._project_counter, name, description)
        self.projects[self._project_counter] = project
        self._project_counter += 1
        return project

    def get_project(self, project_id: int) -> Project:
        project = self.projects.get(project_id)
        if not project:
            raise NotFoundError(f"project {project_id} not found")
        return project

    def update_project(
        self,
        project_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Project:
        project = self.get_project(project_id)
        project.rename(name=name, description=description)
        return project

    def list_projects(self) -> list[Project]:
        return sorted(self.projects.values(), key=lambda p: p.created_at)

    def remove_project(self, project_id: int) -> None:
        """Remove a project and cascade-delete its tasks."""
        if project_id not in self.projects:
            raise NotFoundError(f"project {project_id} not found")
        del self.projects[project_id]

    # --- Task operations -----------------------------------------------
    def add_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: Optional[str] = None,
    ) -> Task:
        project = self.get_project(project_id)

        all_tasks = sum(len(p.tasks) for p in self.projects.values())
        if all_tasks >= TASK_MAX:
            raise ValidationError("maximum number of tasks reached")

        task = Task(self._task_counter, title, description, "todo", deadline)
        project.add_task(task)
        self._task_counter += 1
        return task

    def remove_task(self, project_id: int, task_id: int) -> None:
        project = self.get_project(project_id)
        project.remove_task(task_id)

    def list_tasks(self, project_id: int) -> list[Task]:
        project = self.get_project(project_id)
        return project.list_tasks()

    def change_task_status(self, project_id: int, task_id: int, status: str) -> None:
        project = self.get_project(project_id)
        task = project.get_task(task_id)
        task.change_status(status)

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> None:
        project = self.get_project(project_id)
        task = project.get_task(task_id)
        task.update(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
    # --- Overdue helper ------------------------------------------------
    def iter_overdue(self, today: date | None = None) -> list[Task]:
        """برگرداندن همه تسک‌های دیرکرددار (deadline گذشته و status != done)."""
        if today is None:
            today = date.today()

        overdue_tasks: list[Task] = []

        for project in self.projects.values():
            # فرض می‌کنیم project.list_tasks() لیست Taskها رو می‌ده
            for task in project.list_tasks():
                # اگر deadline نداشت، اصلاً بررسی نمی‌کنیم
                if not task.deadline:
                    continue

                try:
                    # چون تو add_task deadline رو به صورت str می‌فرستی،
                    # فرض می‌کنیم فرمتش YYYY-MM-DD هست و با fromisoformat می‌خونیم.
                    task_deadline = date.fromisoformat(task.deadline)
                except ValueError:
                    # اگر فرمت تاریخ خراب بود، ازش می‌گذریم
                    continue

                if task_deadline < today and task.status != "done":
                    overdue_tasks.append(task)

        return overdue_tasks