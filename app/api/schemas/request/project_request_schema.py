from __future__ import annotations

from pydantic import BaseModel, Field
from app.models.task import MAX_TITLE_LEN, MAX_DESC_LEN


class ProjectCreateRequest(BaseModel):
    """Request body for creating a new project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TITLE_LEN,
        description="Project name (must be unique, non-empty).",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=MAX_DESC_LEN,
        description="Short description of the project.",
    )


class ProjectUpdateRequest(BaseModel):
    """Request body for updating an existing project.

    All fields are optional; only provided fields will be updated.
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_TITLE_LEN,
        description="New project name.",
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_DESC_LEN,
        description="New project description.",
    )
