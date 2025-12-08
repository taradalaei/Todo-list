from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProjectResponse(BaseModel):
    """Standard representation of a project returned by the API."""

    id: int
    name: str
    description: str
    created_at: datetime

    # pydantic v2: allow constructing from dataclass / ORM objects
    model_config = ConfigDict(from_attributes=True)
