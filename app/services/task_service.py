from __future__ import annotations

from datetime import date
from typing import Protocol, Iterable

from app.models.task import Task
from app.exceptions.base import ValidationError, NotFoundError


class TaskStoragePort(Protocol):
    """Interface برای ذخیره/مدیریت Taskها.

    InMemoryStorage فعلی و Repository دیتابیسی بعدی باید این امضاها را پیاده‌سازی کنند.
    """

    def add_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: str | None,
    ) -> Task: ...
    def list_tasks(self, project_id: int) -> Iterable[Task]: ...
    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        deadline: str | None = None,
    ) -> Task: ...
    def change_task_status(
        self,
        project_id: int,
        task_id: int,
        status: str,
    ) -> None: ...
    def remove_task(self, project_id: int, task_id: int) -> None: ...


class TaskService:
    """سرویس برای کار با Taskها."""

    def __init__(self, storage: TaskStoragePort) -> None:
        self._storage = storage

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: str | None,
    ) -> Task:
        return self._storage.add_task(project_id, title, description, deadline)

    def list_tasks(self, project_id: int) -> list[Task]:
        return list(self._storage.list_tasks(project_id))

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        deadline: str | None = None,
    ) -> Task:
        return self._storage.edit_task(
            project_id,
            task_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )

    def change_status(
        self,
        project_id: int,
        task_id: int,
        status: str,
    ) -> None:
        self._storage.change_task_status(project_id, task_id, status)

    def delete_task(self, project_id: int, task_id: int) -> None:
        self._storage.remove_task(project_id, task_id)
