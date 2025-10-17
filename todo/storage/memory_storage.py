
from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

from ..core.project import Project
from ..core.task import Task
from ..core.exceptions import ValidationError, NotFoundError

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

    def list_projects(self) -> list[Project]:
        return sorted(self.projects.values(), key=lambda p: p.created_at)

    def remove_project(self, project_id: int) -> None:
        """Remove a project and cascade-delete its tasks."""
        if project_id not in self.projects:
            raise NotFoundError(f"project {project_id} not found")
        del self.projects[project_id]
