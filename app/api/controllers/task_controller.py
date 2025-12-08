from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.services.task_service import TaskService
from app.exceptions.base import ValidationError, NotFoundError
from app.api.schemas.request.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from app.api.schemas.response.task_response_schema import TaskResponse


class TaskController:
    """Controller for task-related operations.

    This layer maps TaskService to HTTP-friendly models and errors.
    """

    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    # ---------- Read / List ----------------------------------------------

    def list_tasks(self, project_id: int) -> List[TaskResponse]:
        """Return all tasks for a given project."""
        try:
            tasks = self._task_service.list_tasks(project_id)
        except NotFoundError as exc:
            # If the project doesn't exist, storage/service may raise NotFoundError
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        return [TaskResponse.model_validate(t) for t in tasks]

    # ---------- Create ----------------------------------------------------

    def create_task(
        self,
        project_id: int,
        payload: TaskCreateRequest,
    ) -> TaskResponse:
        """Create a new task inside a project."""
        try:
            task = self._task_service.create_task(
                project_id=project_id,
                title=payload.title,
                description=payload.description,
                deadline=payload.deadline,
            )
            return TaskResponse.model_validate(task)
        except NotFoundError as exc:
            # Project not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        except ValidationError as exc:
            # Bad input / invalid deadline / duplicate title
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    # ---------- Update ----------------------------------------------------

    def update_task(
        self,
        project_id: int,
        task_id: int,
        payload: TaskUpdateRequest,
    ) -> TaskResponse:
        """Edit an existing task.

        Uses TaskService.edit_task so we can update title/description/status/deadline.
        """
        try:
            task = self._task_service.edit_task(
                project_id=project_id,
                task_id=task_id,
                title=payload.title,
                description=payload.description,
                status=payload.status,
                deadline=payload.deadline,
            )
            return TaskResponse.model_validate(task)
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

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task from a project."""
        try:
            self._task_service.delete_task(project_id, task_id)
        except NotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
