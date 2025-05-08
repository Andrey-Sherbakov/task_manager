from abc import abstractmethod

from sqlalchemy import select

from src.core.repository import SQLAlchemyORMRepository, IRepository
from src.tasks.models import Task


class ITaskRepository(IRepository[Task]):
    @abstractmethod
    async def get_by_name(self, name: str) -> Task | None: ...


class TaskRepository(SQLAlchemyORMRepository[Task], ITaskRepository):
    model = Task

    async def get_by_name(self, name: str) -> Task | None:
        stmt = select(Task).where(Task.name == name)
        return await self.session.scalar(stmt)
