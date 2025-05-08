from abc import abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.auth.models import User
from src.core.repository import SQLAlchemyORMRepository, IRepository


class IUserRepository(IRepository[User]):
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_by_username_with_tasks(self, username: str) -> User | None: ...


class UserRepository(SQLAlchemyORMRepository[User], IUserRepository):
    model = User

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = await self.session.scalar(stmt)
        return user

    async def get_by_username_with_tasks(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username).options(joinedload(User.tasks))
        user = await self.session.scalar(stmt)
        return user
