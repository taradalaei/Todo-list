from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# 👇 این import فقط برای اینه که مدل‌ها register بشن
# وگرنه ازشون توی این فایل استفاده‌ای نمی‌کنیم
from app.models.orm import ProjectORM, TaskORM  # noqa: F401
