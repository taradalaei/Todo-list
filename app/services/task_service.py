from __future__ import annotations

from datetime import date, datetime
from typing import Protocol, Iterable

from app.models.task import Task, Status
from app.exceptions.base import ValidationError, NotFoundError, InvalidStatusError


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
    def iter_overdue(self, today: date) -> Iterable[Task]:
        """همه تسک‌هایی که deadline < today و status != DONE دارند را برمی‌گرداند."""
        ...


class TaskService:
    """سرویس برای کار با Taskها."""

    def __init__(self, storage: TaskStoragePort) -> None:
        self._storage = storage

    def _validate_deadline(self, deadline: str | None) -> str | None:
        """اعتبارسنجی ددلاین: فرمت و بعد از امروز بودن.

        ورودی: رشته YYYY-MM-DD یا None
        خروجی: همان رشته (اگر معتبر بود) یا raise ValidationError
        """
        if deadline is None:
            return None

        try:
            d = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValidationError("deadline must be in YYYY-MM-DD format") from exc

        # اگر می‌خواهی امروز هم مجاز باشد، این خط را به `if d < date.today():` تغییر بده
        #if d < date.today():
        #    raise ValidationError("deadline can not be in the past")

        return deadline

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: str | None,
    ) -> Task:
        # ✅ چک یونیک بودن عنوان داخل پروژه
        normalized = title.strip().lower()
        for t in self._storage.list_tasks(project_id):
            if t.title.strip().lower() == normalized:
                raise ValidationError(
                    f"task title '{title}' already exists in project {project_id}"
                )

        # ✅ چک اعتبار ددلاین
        deadline = self._validate_deadline(deadline)

        return self._storage.add_task(project_id, title, description, deadline)

    def list_tasks(self, project_id: int) -> list[Task]:
        return list(self._storage.list_tasks(project_id))

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        deadline: str | None = None,
    ) -> Task:
        # ✅ ۱) اگر status جدید داده شده، اول معتبر بودنش را چک می‌کنیم
        if status is not None:
            try:
                status_enum = Status.from_string(status)
            except InvalidStatusError as exc:
                # برای CLI به صورت ValidationError می‌فرستیم
                raise ValidationError(str(exc)) from exc
            # مقدار نرمال‌شده (todo/doing/done) را ذخیره می‌کنیم
            status = status_enum.value

        # ✅ ۲) اگر title جدید داده شده، یکتا بودنش را در همان پروژه چک می‌کنیم
        if title is not None:
            normalized = title.strip().lower()
            for t in self._storage.list_tasks(project_id):
                if t.id != task_id and t.title.strip().lower() == normalized:
                    raise ValidationError(
                        f"task title '{title}' already exists in project {project_id}"
                    )
                
        # ✅ ۳) ولیدیشن ددلاین (اگر مقدار جدیدی داده شده)
        if deadline is not None:
            deadline = self._validate_deadline(deadline)

        # ✅ ۳) بعد از همه‌ی ولیدیشن‌ها، تغییر واقعی را به storage می‌سپاریم
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
        try:
            status_enum = Status.from_string(status)
        except InvalidStatusError as exc:
            raise ValidationError(str(exc)) from exc

        self._storage.change_task_status(
            project_id,
            task_id,
            status_enum.value,
        )

    def delete_task(self, project_id: int, task_id: int) -> None:
        self._storage.remove_task(project_id, task_id)
