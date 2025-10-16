"""Domain-specific exceptions for the ToDo core layer."""


class TaskError(Exception):
    """Base exception for task-related errors."""


class ValidationError(TaskError):
    """Raised when input data fails validation rules."""


class InvalidStatusError(TaskError):
    """Raised when an invalid task status is provided."""


class NotFoundError(TaskError):
    """Raised when an entity is not found in the expected scope."""
