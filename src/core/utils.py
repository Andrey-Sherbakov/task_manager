from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.repository import ITaskRepository, TaskRepository


class IUnitOfWork(ABC):
    tasks: ITaskRepository

    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class AsyncUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: AsyncSession) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "AsyncUnitOfWork":
        self.session = self._session_factory
        self.tasks = TaskRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()
        await self.session.close()
        self.session = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
