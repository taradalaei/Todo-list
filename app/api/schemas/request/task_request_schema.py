from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field
from app.models.task import MAX_TITLE_LEN, MAX_DESC_LEN


class TaskCreateRequest(BaseModel):
    """Request body for creating a new task inside a project."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TITLE_LEN,
        description="Task title (must be unique within the same project).",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=MAX_DESC_LEN,
        description="Task description.",
    )
    # Note: service expects a string deadline (YYYY-MM-DD) or None.
    # We accept a string here; controller later passes it directly to the service.
    deadline: str | None = Field(
        default=None,
        description="Optional deadline in YYYY-MM-DD format.",
    )


class TaskUpdateRequest(BaseModel):
    """Request body for updating an existing task.

    All fields are optional; only provided fields will be updated.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_TITLE_LEN,
        description="New task title.",
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_DESC_LEN,
        description="New task description.",
    )
    status: str | None = Field(
        default=None,
        description="New status: one of 'todo', 'doing', 'done'.",
    )
    deadline: str | None = Field(
        default=None,
        description="New deadline in YYYY-MM-DD format.",
    )
