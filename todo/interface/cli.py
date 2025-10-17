
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
            #print("2. Manage Tasks")
            print("2. Exit")
            choice = input("> ").strip()

            if choice == "1":
                self._project_menu()
            #elif choice == "2":
            #    self._task_menu()
            elif choice == "2":
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
            print(f"[{p.id}] {p.name} — {len(p.tasks)} tasks")

    def _edit_project(self) -> None:
        pid = int(input("Project ID: "))
        name = input("New name (leave blank to skip): ") or None
        desc = input("New description (leave blank to skip): ") or None
        project = self.storage.get_project(pid)
        project.rename(name=name, description=desc)
        print("✅ Project updated.")

    def _delete_project(self) -> None:
        pid = int(input("Project ID to delete: "))
        self.storage.remove_project(pid)
        print("🗑️ Project deleted.")


def main() -> None:
    cli = ToDoCLI()
    cli.run()


if __name__ == "__main__":
    main()
