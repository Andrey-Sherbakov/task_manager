from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import IUserRepository, UserRepository
from src.core.db import async_session_maker
from src.tasks.repository import ITaskRepository, TaskRepository
from src.websocket.utils import ConnectionManager, websocket_manager


class IUnitOfWork(ABC):
    tasks: ITaskRepository
    users: IUserRepository
    websocket: ConnectionManager

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
    def __init__(self) -> None:
        self._session_factory = async_session_maker
        self.session = None

    async def __aenter__(self) -> "AsyncUnitOfWork":
        self.session: AsyncSession = self._session_factory()

        self.tasks = TaskRepository(self.session)
        self.users = UserRepository(self.session)
        self.websocket = websocket_manager

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()
        await self.session.close()
        self.session = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
