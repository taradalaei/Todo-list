# main.py
# This file will be used as the FastAPI entrypoint in Phase 3.
# The previous CLI logic has been moved to cli_main.py.

from __future__ import annotations

from fastapi import FastAPI

from app.api.routers import project_router, task_router


app = FastAPI(
    title="ToDo List API",
    version="3.0.0",
    description=(
        "ToDo List Web API for the Software Engineering course "
        "(Phase 3 - FastAPI based interface)."
    ),
)


# Include routers
app.include_router(project_router)
app.include_router(task_router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Simple health check / welcome endpoint."""
    return {"message": "ToDo List API is running (Phase 3 – Web API)."}
