
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
Phase 2 :

---

# 🗂 ToDo List – Python OOP + SQLAlchemy + PostgreSQL (Phase 2)

فاز دوم پروژه ToDo List که در درس مهندسی نرم‌افزار طراحی شده و شامل مهاجرت کامل از **In-Memory** به **PostgreSQL**، پیاده‌سازی **Repository Pattern**، ساخت **Command** جانبی و اجرای خودکار با **Scheduler** است.

---

# 🚀 Features (Phase 2)

### Domain & Architecture

* OOP domain models: `Task`, `Project`
* Validation rules داخل Domain (عنوان، توضیح، وضعیت، ددلاین)
* جداسازی کامل Domain از Data Layer با **Repository Pattern**
* Service Layer مستقل از ORM

### Persistence & Infrastructure

* ذخیره‌سازی پایدار با **PostgreSQL**
* اجرای دیتابیس داخل **Docker**
* پیاده‌سازی کامل Storage با **SQLAlchemy ORM**
* ساخت و مدیریت تغییرات دیتابیس با **Alembic Migration**

### Application Logic

* پشتیبانی از فیلد جدید: `at_closed` برای ثبت زمان بسته شدن Task
* Command اختصاصی:

  ```
  autoclose_overdue
  ```

  جهت بستن Taskهای دیرکرده

### Automation

* اجرای خودکار Command با کتابخانهٔ **schedule**
* Scheduler قابل اجرا به‌صورت جداگانه (Background Worker)

### CLI

* مدیریت پروژه‌ها و تسک‌ها: ایجاد، ویرایش، حذف، لیست، تغییر وضعیت
* عدم وابستگی CLI به ORM یا دیتابیس (ارتباط فقط از طریق Service)

---

# 📦 Project Structure

```
ToDoList/
├── app/
│   ├── models/          # Domain models & enums
│   ├── services/        # Application services (Project/Task)
│   ├── repositories/    # Storage layer (SQLAlchemy + Ports)
│   ├── commands/        # CLI Commands (autoclose_overdue, scheduler)
│   ├── db/              # ORM models + session + engine
│   └── exceptions/
├── todo/interface/      # CLI user interface
├── migrations/          # Alembic migration versions
├── docker-compose.yml
├── main.py              # CLI entry point
├── .env.example
├── pyproject.toml
└── README.md
```

---

# ⚙️ Setup

## 1. نصب پکیج‌ها

```bash
poetry install
```

## 2. ساخت و اجرای دیتابیس در Docker

```bash
docker compose up -d
```

PostgreSQL با نام کانتینر:

```
todolist-postgres
```

بالا می‌آید.

## 3. اجرای Migrationها

```bash
poetry run alembic upgrade head
```

ستون‌های جدید شامل `at_closed` نیز ایجاد می‌شوند.

## 4. اجرای برنامه CLI

```bash
poetry run python main.py
```

---

# ⚙️ Environment Variables

یک `.env` ایجاد کنید (از `.env.example` کپی کنید):

```
DATABASE_URL=postgresql+psycopg://todolist_user:todolist_password@localhost:5432/todolist_db
PROJECT_OF_NUMBER_MAX=5
TASK_OF_NUMBER_MAX=20
USE_DB=1
```

---

# 🧾 Commands (Phase 2)

## اجرای Command بستن Taskهای دیرکرده

```bash
poetry run python -m app.commands.autoclose_overdue
```

این دستور:

* همه Taskهایی با deadline گذشته
* و وضعیت غیر از DONE
  را پیدا کرده و می‌بندد (`status="done"` + مقداردهی `at_closed`).

---

# ⏱ Scheduler (اجرای خودکار Command)

Scheduler مستقل از main اجرا می‌شود:

```bash
poetry run python -m app.commands.scheduler
```

به صورت پیش‌فرض هر ۱۵ دقیقه دستور autoclose اجرا می‌شود:

```
[scheduler] closed X overdue tasks
```

(برای تست، می‌توانید بازه را ۵ ثانیه کنید.)

---

# 🧱 Repository Pattern

در فاز ۲ پروژه، لایه‌ها این‌گونه جدا شده‌اند:

* **Domain Layer** → `Task`, `Project`
* **Service Layer** → `TaskService`, `ProjectService`
* **Repository Layer** → `SqlAlchemyStorage` و `InMemoryStorage`
* **ORM Layer** → `TaskORM`, `ProjectORM`

سرویس‌ها **هیچ دانشی** نسبت به دیتابیس یا SQLAlchemy ندارند و فقط با **Port** حرف می‌زنند:

```python
class TaskStoragePort(Protocol):
    def add_task(...): ...
    def list_tasks(...): ...
    ...
```

این همان Repository Pattern است.

---

# 🧪 Testing (Phase 2)

* ایجاد پروژه و تسک با CLI
* تغییر وضعیت و تست مقداردهی خودکار `at_closed`
* ایجاد یک Task با deadline گذشته → اجرای autoclose → بررسی در DB
* اجرای Scheduler → مشاهده اجرای خودکار عملیات

---

# 🛠 Next Steps (Phase 3)

* پیاده‌سازی FastAPI
* JWT Authentication
* Swagger/OpenAPI
* Unit Tests & Integration Tests

--- 

## CLI Status and Phase 3 (Web API)

In Phase 3 of this project, the Command Line Interface (CLI) has been **deprecated**.  
The primary interface of the system from this phase onward is a **Web API** built with FastAPI.

- The CLI is still available in this version, but it is only kept for backward compatibility.
- The CLI will not receive further updates and may be removed in future releases.
- For all new features and interactions, it is recommended to use the Web API.

### Running the Web API

To run the Web API (the main interface for Phase 3), execute:

```bash
poetry run uvicorn main:app --reload
````

After starting the server, the automatically generated API documentation will be available at:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

### Running the CLI (Legacy – Deprecated)

The Command Line Interface remains available in this version, but it is **deprecated** and no longer actively maintained.

To run the legacy CLI (if needed), use the following command (assuming you moved the old CLI entrypoint to `cli_main.py`):

```bash
poetry run python cli_main.py
```

---

Made with ❤️ by **Tara Dalaei**