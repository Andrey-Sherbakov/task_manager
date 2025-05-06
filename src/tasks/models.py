import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None, nullable=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
