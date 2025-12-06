from todo.interface.cli import ToDoCLI
from todo.storage.memory_storage import InMemoryStorage

def main() -> None:
    storage = InMemoryStorage()     # ✅ ساخت وابستگی در Main
    cli = ToDoCLI(storage)          # ✅ تزریق به CLI
    cli.run()

if __name__ == "__main__":
    main()
