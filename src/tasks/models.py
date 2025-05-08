import datetime

from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None, nullable=True)
    creator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    creator: Mapped["User"] = relationship(back_populates="tasks")
