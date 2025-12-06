from todo.interface.cli import ToDoCLI
from todo.storage.memory_storage import InMemoryStorage

from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def main() -> None:
    # لایه‌ی ذخیره‌سازی
    storage = InMemoryStorage()

    # لایه‌ی سرویس (DI: storage تزریق می‌شود)
    project_service = ProjectService(storage)
    task_service = TaskService(storage)

    # لایه‌ی CLI (DI: service ها تزریق می‌شوند)
    cli = ToDoCLI(
        project_service=project_service,
        task_service=task_service,
    )
    cli.run()

if __name__ == "__main__":
    main()
