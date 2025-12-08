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

        # crucial
        if d < date.today():
            raise ValidationError("deadline can not be in the past")

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
        """لیست تسک‌های یک پروژه را برمی‌گرداند.

        نکته: در حال حاضر فقط خروجی storage را wrap می‌کند.
        اگر بخواهی در صورت نبودن پروژه 404 بدهی، باید در لایه‌ی storage
        (یا در سرویسی که پروژه را مدیریت می‌کند) NotFoundError را raise کنی
        و این متد همان را به بالا پاس بدهد.
        """
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
        """ویرایش تسک.

        - title و description و deadline مستقیم از طریق edit_task استوریج آپدیت می‌شوند.
        - تغییر status از طریق change_task_status انجام می‌شود تا منطق at_closed
          در همان جای اصلی (Repository/Storage) اجرا شود.
        """

        status_enum: Status | None = None

        # ✅ ۱) اگر status جدید داده شده، اول معتبر بودنش را چک می‌کنیم
        if status is not None:
            try:
                status_enum = Status.from_string(status)
            except InvalidStatusError as exc:
                # برای لایه‌های بالاتر (CLI/API) به صورت ValidationError می‌فرستیم
                raise ValidationError(str(exc)) from exc

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

        # ✅ ۴) ابتدا فقط title/description/deadline را از طریق edit_task آپدیت می‌کنیم
        #       (status را اینجا به storage نمی‌دهیم تا منطق at_closed به هم نخورد)
        task = self._storage.edit_task(
            project_id,
            task_id,
            title=title,
            description=description,
            status=None,
            deadline=deadline,
        )

        # ✅ ۵) اگر status جدید داده شده، از مسیر رسمی change_task_status می‌رویم
        #       تا منطق at_closed در همان‌جا (Repository) اجرا شود.
        if status_enum is not None:
            try:
                self._storage.change_task_status(
                    project_id,
                    task_id,
                    status_enum.value,
                )
            except NotFoundError:
                # اگر در این مرحله تسک یا پروژه پیدا نشد، همان خطا را به بالا پاس می‌دهیم
                raise

            # بعد از تغییر status، نسخه‌ی به‌روز تسک را دوباره از storage می‌خوانیم
            for t in self._storage.list_tasks(project_id):
                if t.id == task_id:
                    task = t
                    break

        return task

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
