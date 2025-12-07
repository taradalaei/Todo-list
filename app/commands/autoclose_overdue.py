from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.orm import TaskORM


def run() -> int:
    """بستن خودکار تسک‌های دیرکرددار در دیتابیس.
    همه تسک‌هایی که deadline < today و status != 'done' هستند را
    به حالت 'done' می‌برد و at_closed را تنظیم می‌کند.
    تعداد تسک‌های بسته شده را برمی‌گرداند.
    """
    today = date.today()
    closed_count = 0

    # SessionLocal را از app/db/session.py می‌گیریم
    with SessionLocal() as session:
        stmt = (
            select(TaskORM)
            .where(
                TaskORM.deadline < today,
                TaskORM.status != "done",
            )
        )

        for task in session.scalars(stmt):
            task.status = "done"
            task.at_closed = datetime.utcnow()
            closed_count += 1

        session.commit()

    return closed_count


if __name__ == "__main__":
    count = run()
    print(f"{count} overdue tasks closed.")
