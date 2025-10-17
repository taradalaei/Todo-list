
# 🗂 ToDo List - Python OOP (In-Memory)

Phase 1 of a modular ToDo List system built for AUT Software Engineering Course.

## 🚀 Features
- OOP design with clear domain models (`Task`, `Project`)
- In-memory storage layer
- CLI interface for interaction
- Type hints, docstrings, and code conventions (PEP8)
- Extensible for future persistence and FastAPI integration

## 🧱 Project Structure
```
todo_list/
├── todo/
│   ├── core/
│   ├── storage/
│   └── interface/
├── main.py
├── .env.example
├── pyproject.toml
├── CODESTYLE.md
└── README.md
```

## ⚙️ Setup & Run
1. **Install dependencies**  
   ```bash
   poetry install
   ```

2. **Run the app**  
   ```bash
   poetry run python main.py
   ```

3. **Environment Variables**  
   Copy `.env.example` to `.env` and adjust values if needed:
   ```bash
   PROJECT_OF_NUMBER_MAX=5
   TASK_OF_NUMBER_MAX=20
   ```

## 🧠 Next Phases
- Add persistence (JSON/SQLite)
- Build FastAPI REST backend
- Write automated tests (pytest)

---
Made with ❤️ by Tara Dalaei