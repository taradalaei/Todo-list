from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional

from .exceptions import InvalidStatusError, ValidationError


class Status(str, Enum):
    """Allowed task statuses."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"

    @classmethod
    def from_string(cls, value: str) -> "Status":
        try:
            return cls(value.lower())
        except ValueError as exc:
            raise InvalidStatusError(f"invalid status: {value!r}") from exc


MAX_TITLE_LEN = 30
MAX_DESC_LEN = 150


def _parse_deadline(raw: Optional[str]) -> Optional[date]:
    if raw is None or raw == "":
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError(
            "deadline must be in YYYY-MM-DD format and a valid date"
        ) from exc


@dataclass(slots=True)
class Task:
    """Represents an individual task in a project.

    Validation rules:
    - title length >= 30
    - description length >= 150
    - status in {todo, doing, done}
    - deadline (if provided) must be a valid YYYY-MM-DD date
    """

    id: int
    title: str
    description: str
    status: Status = field(default=Status.TODO)
    deadline: Optional[date] = field(default=None)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValidationError("task title cannot be empty")
        if len(self.title) > MAX_TITLE_LEN:
            raise ValidationError(
                f"title must be maximum {MAX_TITLE_LEN} characters"
            )
        if len(self.description) > MAX_DESC_LEN:
            raise ValidationError(
                f"description must be maximum {MAX_DESC_LEN} characters"
            )
        # Ensure status is a Status enum (accept string for convenience)
        if isinstance(self.status, str):
            self.status = Status.from_string(self.status)
        elif not isinstance(self.status, Status):
            raise InvalidStatusError("status must be a Status or valid string")

    # --- Mutators -----------------------------------------------------
    def change_status(self, new_status: Status | str) -> None:
        """Change task status after validating allowed values."""
        self.status = (
            Status.from_string(new_status)
            if isinstance(new_status, str)
            else Status(new_status.value)  # ensure valid member
        )

    def update(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[Status | str] = None,
        deadline: Optional[str | date | None] = None,
    ) -> None:
        """Update mutable fields with validation.

        Keyword-only to keep the signature clear and stable.
        - If deadline is a string, it must be YYYY-MM-DD; date is accepted too.
        """
        if title is not None:
            if len(title) > MAX_TITLE_LEN:
                raise ValidationError(
                    f"title must be maximum {MAX_TITLE_LEN} characters"
                )
            self.title = title

        if description is not None:
            if len(description) > MAX_DESC_LEN:
                raise ValidationError(
                    f"description must be maximum {MAX_DESC_LEN} characters"
                )
            self.description = description

        if status is not None:
            self.change_status(status)

        if deadline is not None:
            try:
                deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    f"Deadline '{deadline}' is invalid. Use YYYY-MM-DD format."
                )

            # 4️⃣ Check if deadline is in the past
            if deadline_dt.date() < datetime.now().date():
                raise ValidationError("Deadline cannot be in the past.")

            # Optional: if you have a project start date
            if hasattr(self, 'start_date') and deadline_dt.date() < self.start_date:
                raise ValidationError("Deadline cannot be before project start date.")

            ## Store the parsed datetime if you want consistent type
            #task.deadline = deadline_dt

            if isinstance(deadline, date):
                self.deadline = deadline
            else:
                self.deadline = _parse_deadline(deadline)
