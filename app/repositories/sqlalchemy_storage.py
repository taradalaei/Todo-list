from __future__ import annotations

from typing import Iterable
from datetime import date, datetime


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task
from app.models.orm import ProjectORM, TaskORM
from app.exceptions.base import NotFoundError, ValidationError
from app.services.project_service import ProjectStoragePort
from app.services.task_service import TaskStoragePort


class SqlAlchemyStorage(ProjectStoragePort, TaskStoragePort):
    """پیاده‌سازی دیتابیسی Storage با استفاده از SQLAlchemy.

    این کلاس همزمان هم ProjectStoragePort و هم TaskStoragePort را پیاده‌سازی می‌کند،
    مثل InMemoryStorage، اما داده‌ها را در PostgreSQL نگه می‌دارد.
    """

    def __init__(self, session: Session) -> None:
        # ⛔ این‌جا Session ساخته نمی‌شود، از بیرون تزریق می‌شود (DI)
        self.session = session

    # ------------- Project متدهای  ---------------------------------

    def _parse_deadline(self, deadline: str | None) -> date | None:
        """تبدیل رشته YYYY-MM-DD به date. اگر خالی بود → None.

        اگر فرمت اشتباه باشد، ValidationError می‌اندازد تا CLI بتواند پیام مناسب نشان بدهد.
        """
        if not deadline:
            return None

        try:
            return datetime.strptime(deadline.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                f"invalid deadline format: '{deadline}'. Expected YYYY-MM-DD (e.g. 2025-12-31)"
            )

    def add_project(self, name: str, description: str) -> Project:
        orm = ProjectORM(name=name, description=description)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return Project(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            tasks=[],
        )

    def list_projects(self) -> Iterable[Project]:
        stmt = select(ProjectORM).order_by(ProjectORM.id)
        result = self.session.execute(stmt)
        for row in result.scalars():
            yield Project(
                id=row.id,
                name=row.name,
                description=row.description,
                tasks=[],  # اگر خواستیم، بعداً می‌تونیم taskها رو هم map کنیم
            )

    def get_project(self, project_id: int) -> Project:
        orm = self.session.get(ProjectORM, project_id)
        if orm is None:
            raise NotFoundError(f"project with id={project_id} not found")

        # اگر خواستی taskها رو هم اضافه کنی، این‌جا می‌تونی map کنی.
        return Project(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            tasks=[],
        )

    def update_project(
        self,
        project_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Project:
        orm = self.session.get(ProjectORM, project_id)
        if orm is None:
            raise NotFoundError(f"project with id={project_id} not found")

        if name is not None:
            orm.name = name
        if description is not None:
            orm.description = description

        self.session.commit()
        self.session.refresh(orm)

        return Project(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            tasks=[],
        )

    def remove_project(self, project_id: int) -> None:
        orm = self.session.get(ProjectORM, project_id)
        if orm is None:
            raise NotFoundError(f"project with id={project_id} not found")

        self.session.delete(orm)
        self.session.commit()

    # ------------- Task متدهای  ------------------------------------

    def add_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: str | None,
    ) -> Task:
        deadline_date = self._parse_deadline(deadline)

        orm = TaskORM(
            project_id=project_id,
            title=title,
            description=description,
            status="todo",
            deadline=deadline_date,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)

        return Task(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            status=orm.status,
            deadline=orm.deadline,
        )

    def list_tasks(self, project_id: int) -> Iterable[Task]:
        stmt = select(TaskORM).where(TaskORM.project_id == project_id).order_by(TaskORM.id)
        result = self.session.execute(stmt)
        for orm in result.scalars():
            yield Task(
                id=orm.id,
                title=orm.title,
                description=orm.description,
                status=orm.status,
                deadline=orm.deadline,
            )

    def _get_task_orm(self, project_id: int, task_id: int) -> TaskORM:
        stmt = select(TaskORM).where(
            TaskORM.id == task_id,
            TaskORM.project_id == project_id,
        )
        result = self.session.execute(stmt).scalar_one_or_none()
        if result is None:
            raise NotFoundError(f"task with id={task_id} in project {project_id} not found")
        return result

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        deadline: str | None = None,
    ) -> Task:
        orm = self._get_task_orm(project_id, task_id)

        # اینجا ORM را آپدیت می‌کنیم، منطق اعتبارسنجی را می‌گذاریم گردن دامنه (Task)
        if title is not None:
            orm.title = title
        if description is not None:
            orm.description = description
        if status is not None:
            orm.status = status
        if deadline is not None:
            orm.deadline = self._parse_deadline(deadline)

        self.session.commit()
        self.session.refresh(orm)

        return Task(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            status=orm.status,
            deadline=orm.deadline,
        )

    def change_task_status(
        self,
        project_id: int,
        task_id: int,
        status: str,
    ) -> None:
        orm = self._get_task_orm(project_id, task_id)
        orm.status = status
        self.session.commit()

    def remove_task(self, project_id: int, task_id: int) -> None:
        orm = self._get_task_orm(project_id, task_id)
        self.session.delete(orm)
        self.session.commit()
