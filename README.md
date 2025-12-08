# 🗂 ToDo List – Modular Python Project (OOP → SQLAlchemy → FastAPI)

A fully modular ToDo List system developed across **three phases** for the AUT Software Engineering Course.
The project evolves from a simple in-memory CLI tool to a fully layered architecture with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Repository Pattern**, and **Background Scheduler**.

---

# 📌 Table of Contents

1. Phase 1 – OOP & In-Memory
2. Phase 2 – PostgreSQL, SQLAlchemy ORM, Repository Pattern, Commands
3. Phase 3 – FastAPI Web API (Primary Interface)
4. Project Structure
5. Setup & Installation
6. Running the CLI (Legacy)
7. Running the Web API (Phase 3)
8. API Endpoints (Summary)
9. Environment Variables
10. Future Work
11. Author

---

# 🧩 Phase 1 – OOP & In-Memory Implementation

The foundation of the system was built using **pure Python OOP principles**:

### 🚀 Features

* Domain models:

  * `Task`
  * `Project`
* In-memory storage
* CLI interaction
* Input validation inside domain classes
* Type hints, docstrings, PEP8 conventions
* Designed for clean extensibility into future phases

---

# 🧩 Phase 2 – SQLAlchemy, PostgreSQL, Repository Pattern, Commands

Phase 2 migrates the system from in-memory to a **persistent**, database-backed architecture.

### 🚀 Major Features (Phase 2)

#### Domain & Architecture

* Domain models unchanged (`Task`, `Project`, `Status`)
* Validation rules enforced inside domain
* Full **Repository Pattern**
* Service Layer independent of persistence mechanism

#### Persistence Layer

* PostgreSQL database
* Docker-based infrastructure
* SQLAlchemy ORM models for `Project` and `Task`
* Alembic migrations for DB schema

#### Application Logic Enhancements

* New field: `at_closed` (timestamp when task is marked done)
* Automatic closing of overdue tasks via command:

```bash
poetry run python -m app.commands.autoclose_overdue
```

#### Background Scheduler

Runs the autoclose command periodically:

```bash
poetry run python -m app.commands.scheduler
```

---

# 🧩 Phase 3 – FastAPI Web API (Primary Interface)

In Phase 3, the main interface of the project becomes a **RESTful Web API** powered by FastAPI.
The CLI is now **deprecated** (still available for backward compatibility).

### 🚀 Features (Phase 3)

* Complete REST API for Projects & Tasks:

  * Create / List / Update / Delete Projects
  * Create / List / Update / Delete Tasks inside Projects
* Fully layered architecture:

  * **API Layer** → routers, controllers, Pydantic schemas
  * **Service Layer** → business logic
  * **Repository Layer** → SQLAlchemy storage
  * **Domain Layer** → models, enums, validation
* Automatic request validation via Pydantic
* Consistent HTTP responses:

  * `400` – domain validation errors
  * `404` – resource not found
  * `422` – schema validation errors
* Auto-generated API documentation:

  * Swagger UI → `/docs`
  * ReDoc → `/redoc`
* Deadline field is optional for tasks
* Business logic for `at_closed` is preserved from Phase 2
* Schedule & autoclose command remain external (CLI-based), independent of the Web API

---

# 📦 Project Structure (Phase 3 – Final)

```text
ToDoList/
├── app/
│   ├── api/                     # Phase 3 Web API (FastAPI)
│   │   ├── controllers/         # Connect API ↔ Services
│   │   ├── routers/             # API routes (projects, tasks)
│   │   └── schemas/
│   │       ├── request/         # Pydantic input models
│   │       └── response/        # Pydantic output models
│   ├── models/                  # Domain models (Task, Project, Status)
│   ├── services/                # Business logic (ProjectService, TaskService)
│   ├── repositories/            # Storage (SQLAlchemy implementation)
│   ├── commands/                # CLI commands (autoclose, scheduler)
│   ├── db/                      # ORM models + engine + session
│   └── exceptions/              # Domain-level errors
│
├── todo/interface/              # Legacy CLI (deprecated in Phase 3)
│
├── migrations/                  # Alembic migrations
├── docker-compose.yml
├── main.py                      # FastAPI entrypoint
├── cli_main.py                  # Legacy CLI entrypoint
├── pyproject.toml
├── .env.example
└── README.md
```

---

# ⚙️ Setup & Installation

### 1. Install dependencies

```bash
poetry install
```

### 2. Start PostgreSQL with Docker

```bash
docker compose up -d
```

### 3. Run database migrations

```bash
poetry run alembic upgrade head
```

---

# 🖥 Running the CLI (Legacy – Deprecated)

The CLI is still available but will be removed in future releases.

```bash
poetry run python cli_main.py
```

A deprecation warning is shown when launched.

---

# 🌐 Running the Web API (Phase 3)

The FastAPI Web API is the **primary interface** of the system starting in Phase 3.

### Start the server:

```bash
poetry run uvicorn main:app --reload
```

### API Documentation:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# 📡 API Endpoints (Summary)

### Projects

| Method | Endpoint             | Description        |
| ------ | -------------------- | ------------------ |
| GET    | `/api/projects`      | List all projects  |
| POST   | `/api/projects`      | Create new project |
| PUT    | `/api/projects/{id}` | Update a project   |
| DELETE | `/api/projects/{id}` | Delete a project   |

### Tasks

| Method | Endpoint                                | Description             |
| ------ | --------------------------------------- | ----------------------- |
| GET    | `/api/projects/{project_id}/tasks`      | List tasks of a project |
| POST   | `/api/projects/{project_id}/tasks`      | Create new task         |
| PUT    | `/api/projects/{project_id}/tasks/{id}` | Update a task           |
| DELETE | `/api/projects/{project_id}/tasks/{id}` | Delete a task           |

---

# ⚙️ Environment Variables

Copy `.env.example` → `.env` and set:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/todolist_db
PROJECT_OF_NUMBER_MAX=5
TASK_OF_NUMBER_MAX=20
USE_DB=1
```

---

# 🔮 Future Work

* JWT Authentication + Role-based Authorization
* Unit tests & integration tests
* Pagination for large lists
* Optional frontend (React/Vue)
* Convert autoclose command into a dedicated API endpoint (optional)

---

# ✨ Author

Made with ❤️ by **Tara Dalaei**

---