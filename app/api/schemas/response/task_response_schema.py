from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.models.task import Status


class TaskResponse(BaseModel):
    """Standard representation of a task returned by the API."""

    id: int
    title: str
    description: str
    status: Status
    deadline: date | None = None
    at_closed: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
