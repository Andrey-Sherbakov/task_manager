from abc import ABC, abstractmethod

from sqlalchemy import select

from src.core.repository import SQLAlchemyORMRepository, IRepository
from src.tasks.models import Task


class ITaskRepository(IRepository, ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Task | None: ...


class TaskRepository(SQLAlchemyORMRepository, ITaskRepository):
    model = Task

    async def get_by_name(self, name: str) -> Task | None:
        stmt = select(Task).where(Task.name == name)
        return await self.session.scalar(stmt)
