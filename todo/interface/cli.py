
from __future__ import annotations

from ..storage.memory_storage import InMemoryStorage
from ..core.exceptions import ValidationError, NotFoundError


class ToDoCLI:
    """Command-line interface for the ToDoList app."""

    def __init__(self) -> None:
        self.storage = InMemoryStorage()

    # --- Main loop --------------------------------------------------------
    def run(self) -> None:
        """Main CLI loop."""
        while True:
            print("\n=== ToDoList CLI ===")
            print("1. Manage Projects")
            print("2. Manage Tasks")
            print("3. Exit")
            choice = input("> ").strip()

            if choice == "1":
                self._project_menu()
            elif choice == "2":
                self._task_menu()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    # --- Project Menu -----------------------------------------------------
    def _project_menu(self) -> None:
        while True:
            print("\n--- Project Menu ---")
            print("1. Create Project")
            print("2. List Projects")
            print("3. Edit Project")
            print("4. Delete Project")
            print("5. Back")
            choice = input("> ").strip()

            try:
                if choice == "1":
                    self._create_project()
                elif choice == "2":
                    self._list_projects()
                elif choice == "3":
                    self._edit_project()
                elif choice == "4":
                    self._delete_project()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")
            except (ValidationError, NotFoundError) as err:
                print(f"Error: {err}")

    # --- Project Operations ----------------------------------------------
    def _create_project(self) -> None:
        name = input("Project name: ")
        description = input("Description: ")
        project = self.storage.add_project(name, description)
        print(f"✅ Created project #{project.id}: {project.name}")

    def _list_projects(self) -> None:
        projects = self.storage.list_projects()
        if not projects:
            print("No projects found.")
            return
        for p in projects:
            print(f"[{p.id}] {p.name}: {p.description} — {len(p.tasks)} tasks")

    def _edit_project(self) -> None:
        pid = int(input("Project ID: "))
        name = input("New name (leave blank to skip): ") or None
        desc = input("New description (leave blank to skip): ") or None
        project = self.storage.get_project(pid)

        if(name is not None):
            if any(p.name.strip().lower() == name.strip().lower() for p in self.storage.projects.values()):
                raise ValidationError(f"project name '{name}' already exists")
        
        project.rename(name=name, description=desc)
        print("✅ Project updated.")

    def _delete_project(self) -> None:
        pid = int(input("Project ID to delete: "))
        self.storage.remove_project(pid)
        print("🗑️ Project deleted.")

    # --- Task Menu --------------------------------------------------------
    def _task_menu(self) -> None:
        while True:
            print("\n--- Task Menu ---")
            print("1. Add Task")
            print("2. Edit Task")
            print("3. Change Status")
            print("4. Delete Task")
            print("5. List Tasks by Project")
            print("6. Back")
            choice = input("> ").strip()

            try:
                if choice == "1":
                    self._add_task()
                elif choice == "2":
                    self._edit_task()
                elif choice == "3":
                    self._change_status()
                elif choice == "4":
                    self._delete_task()
                elif choice == "5":
                    self._list_tasks()
                elif choice == "6":
                    break
                else:
                    print("Invalid choice.")
            except (ValidationError, NotFoundError) as err:
                print(f"Error: {err}")

    # --- Task Operations --------------------------------------------------
    def _add_task(self) -> None:
        pid = int(input("Project ID: "))
        title = input("Task title: ")
        desc = input("Task description: ")
        deadline = input("Deadline (YYYY-MM-DD or blank): ") or None
        task = self.storage.add_task(pid, title, desc, deadline)
        print(f"✅ Added task #{task.id} to project #{pid}")

    def _edit_task(self) -> None:
        pid = int(input("Project ID: "))
        tid = int(input("Task ID: "))
        title = input("New title (blank to skip): ") or None
        desc = input("New description (blank to skip): ") or None
        status = input("New status [todo/doing/done] (blank to skip): ") or None
        deadline = input("New deadline (YYYY-MM-DD or blank): ") or None
        self.storage.edit_task(pid, tid, title=title, description=desc, status=status, deadline=deadline)
        print("✅ Task updated.")

    def _change_status(self) -> None:
        pid = int(input("Project ID: "))
        tid = int(input("Task ID: "))
        status = input("New status [todo/doing/done]: ")
        self.storage.change_task_status(pid, tid, status)
        print("✅ Status changed.")

    def _delete_task(self) -> None:
        pid = int(input("Project ID: "))
        tid = int(input("Task ID: "))
        self.storage.remove_task(pid, tid)
        print("🗑️ Task deleted.")

    def _list_tasks(self) -> None:
        pid = int(input("Project ID: "))
        tasks = self.storage.list_tasks(pid)
        if not tasks:
            print("No tasks found in this project.")
            return
        for t in tasks:
            deadline = getattr(t.deadline, "isoformat", lambda: str(t.deadline))() if t.deadline else "-"
            print(f"[{t.id}] {t.title[:25]} | {t.status.upper()} | {deadline}")


def main() -> None:
    cli = ToDoCLI()
    cli.run()


if __name__ == "__main__":
    main()
