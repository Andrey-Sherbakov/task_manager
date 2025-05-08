from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    fullname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    age: Mapped[int | None] = mapped_column(nullable=True)

    tasks: Mapped[list["Task"]] = relationship(back_populates="creator", order_by="Task.id.desc()")
