from __future__ import annotations

from typing import Protocol, Iterable

from app.models.project import Project
from app.exceptions.base import ValidationError, NotFoundError


class ProjectStoragePort(Protocol):
    """Interface (پورت) برای چیزهایی که پروژه‌ها را ذخیره می‌کنند."""

    def add_project(self, name: str, description: str) -> Project: ...
    def list_projects(self) -> Iterable[Project]: ...
    def get_project(self, project_id: int) -> Project: ...
    def remove_project(self, project_id: int) -> None: ...


class ProjectService:
    """سرویس برای عملیات روی Project."""

    def __init__(self, storage: ProjectStoragePort) -> None:
        self._storage = storage

    def create_project(self, name: str, description: str) -> Project:
        return self._storage.add_project(name, description)

    def list_projects(self) -> list[Project]:
        return list(self._storage.list_projects())

    def rename_project(
        self,
        project_id: int,
        new_name: str | None = None,
        new_description: str | None = None,
    ) -> Project:
        project = self._storage.get_project(project_id)

        # ✅ اینجا چک می‌کنیم اسم تکراری نباشه
        if new_name is not None:
            normalized = new_name.strip().lower()
            for p in self._storage.list_projects():
                if p.id != project_id and p.name.strip().lower() == normalized:
                    raise ValidationError(f"project name '{new_name}' already exists")

        project.rename(name=new_name, description=new_description)
        return project

    def delete_project(self, project_id: int) -> None:
        self._storage.remove_project(project_id)
