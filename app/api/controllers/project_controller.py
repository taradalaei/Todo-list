from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.exceptions.base import ValidationError, NotFoundError
from app.api.schemas.request.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from app.api.schemas.response.project_response_schema import ProjectResponse


class ProjectController:
    """Controller for project-related operations.

    This layer converts domain/service objects and exceptions
    into API-friendly responses and HTTP errors.
    """

    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService | None = None,
    ) -> None:
        self._project_service = project_service
        # task_service is optional for now; may be used later
        self._task_service = task_service

    # ---------- Read / List ----------------------------------------------

    def list_projects(self) -> List[ProjectResponse]:
        """Return all projects as API response models."""
        projects = self._project_service.list_projects()
        return [ProjectResponse.model_validate(p) for p in projects]

    # ---------- Create ----------------------------------------------------

    def create_project(
        self,
        payload: ProjectCreateRequest,
    ) -> ProjectResponse:
        """Create a new project and return it.

        Maps ValidationError from the service to HTTP 400.
        """
        try:
            project = self._project_service.create_project(
                name=payload.name,
                description=payload.description,
            )
            return ProjectResponse.model_validate(project)
        except ValidationError as exc:
            # Bad input from the client
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    # ---------- Update ----------------------------------------------------

    def update_project(
        self,
        project_id: int,
        payload: ProjectUpdateRequest,
    ) -> ProjectResponse:
        """Update an existing project.

        Only fields provided in the payload will be changed.
        """
        try:
            project = self._project_service.rename_project(
                project_id=project_id,
                new_name=payload.name,
                new_description=payload.description,
            )
            return ProjectResponse.model_validate(project)
        except NotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    # ---------- Delete ----------------------------------------------------

    def delete_project(self, project_id: int) -> None:
        """Delete a project.

        Returns None; the router will typically use HTTP 204.
        """
        try:
            self._project_service.delete_project(project_id)
        except NotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
