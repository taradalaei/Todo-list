"""
Legacy CLI Entrypoint (Deprecated)
This interface is deprecated and will be removed in future releases.
"""

from __future__ import annotations

import os

from todo.interface.cli import ToDoCLI
from todo.storage.memory_storage import InMemoryStorage

from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.db.session import get_session
# from app.repositories.sqlalchemy_storage import SqlAlchemyStorage


def build_storage():
    """انتخاب پیاده‌سازی Storage بر اساس تنظیمات."""
    use_db = os.getenv("USE_DB", "0") == "1"

    if use_db:
        # ⭐ فقط وقتی نیاز داریم import می‌کنیم (تا circular import بی‌خودی نشه)
        from app.repositories.sqlalchemy_storage import SqlAlchemyStorage

        session = get_session()
        storage = SqlAlchemyStorage(session)
        return storage, session
    else:
        storage = InMemoryStorage()
        return storage, None



def main() -> None:

    print(
        "[DEPRECATION WARNING] The CLI interface is deprecated. "
        "Please use the FastAPI Web API instead."
    )

    storage, session = build_storage()

    # لایه‌ی سرویس‌ها (DI: storage تزریق می‌شود)
    project_service = ProjectService(storage)
    task_service = TaskService(storage)

    # لایه‌ی CLI (DI: سرویس‌ها تزریق می‌شوند)
    cli = ToDoCLI(
        project_service=project_service,
        task_service=task_service,
    )

    try:
        cli.run()
    finally:
        # اگر با DB کار می‌کنیم، Session را ببندیم
        if session is not None:
            session.close()


if __name__ == "__main__":
    main()
