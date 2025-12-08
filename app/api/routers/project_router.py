from __future__ import annotations

from typing import Generator

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.sqlalchemy_storage import SqlAlchemyStorage
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.api.controllers.project_controller import ProjectController
from app.api.schemas.request.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from app.api.schemas.response.project_response_schema import ProjectResponse


router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
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


def get_project_controller(
    storage: SqlAlchemyStorage = Depends(get_storage),
) -> ProjectController:
    """Wire up ProjectService/TaskService into the controller."""
    project_service = ProjectService(storage)
    task_service = TaskService(storage)
    return ProjectController(
        project_service=project_service,
        task_service=task_service,
    )


# ----------------------
# Endpoints
# ----------------------
@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="List all projects",
)
def list_projects(
    controller: ProjectController = Depends(get_project_controller),
):
    return controller.list_projects()


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(
    payload: ProjectCreateRequest,
    controller: ProjectController = Depends(get_project_controller),
):
    return controller.create_project(payload)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update an existing project",
)
def update_project(
    project_id: int,
    payload: ProjectUpdateRequest,
    controller: ProjectController = Depends(get_project_controller),
):
    return controller.update_project(project_id, payload)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(
    project_id: int,
    controller: ProjectController = Depends(get_project_controller),
):
    controller.delete_project(project_id)
