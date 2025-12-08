from __future__ import annotations

from typing import Generator

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.sqlalchemy_storage import SqlAlchemyStorage
from app.services.task_service import TaskService
from app.api.controllers.task_controller import TaskController
from app.api.schemas.request.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from app.api.schemas.response.task_response_schema import TaskResponse


router = APIRouter(
    prefix="/api/projects/{project_id}/tasks",
    tags=["tasks"],
)


# ----------------------
# Dependencies (DI)
# ----------------------
def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session per request."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def get_storage(db: Session = Depends(get_db)) -> SqlAlchemyStorage:
    """Provide a SqlAlchemyStorage instance per request."""
    return SqlAlchemyStorage(db)


def get_task_controller(
    storage: SqlAlchemyStorage = Depends(get_storage),
) -> TaskController:
    """Wire up TaskService into the controller."""
    task_service = TaskService(storage)
    return TaskController(task_service=task_service)


# ----------------------
# Endpoints
# ----------------------
@router.get(
    "",
    response_model=list[TaskResponse],
    summary="List all tasks in a project",
)
def list_tasks(
    project_id: int,
    controller: TaskController = Depends(get_task_controller),
):
    return controller.list_tasks(project_id)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task in a project",
)
def create_task(
    project_id: int,
    payload: TaskCreateRequest,
    controller: TaskController = Depends(get_task_controller),
):
    return controller.create_task(project_id, payload)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update an existing task",
)
def update_task(
    project_id: int,
    task_id: int,
    payload: TaskUpdateRequest,
    controller: TaskController = Depends(get_task_controller),
):
    return controller.update_task(project_id, task_id, payload)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    project_id: int,
    task_id: int,
    controller: TaskController = Depends(get_task_controller),
):
    controller.delete_task(project_id, task_id)
