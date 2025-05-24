from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy import select, Sequence, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import Base

T = TypeVar("T", bound=Base)


class IRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, item_id: int) -> T | None: ...

    @abstractmethod
    async def get_all(self) -> Sequence[T]: ...

    @abstractmethod
    async def create(self, item: BaseModel) -> T: ...

    @abstractmethod
    async def update_by_id(self, item_id: int, item: BaseModel) -> T | None: ...

    @abstractmethod
    async def delete_by_id(self, item_id: int) -> T | None: ...


class SQLAlchemyORMRepository(IRepository[T]):
    model: T

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == item_id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[T]:
        stmt = select(self.model)
        items = await self.session.scalars(stmt)
        return items.all()

    async def create(self, item: BaseModel) -> T:
        stmt = insert(self.model).values(**item.model_dump()).returning(self.model)
        new_item = await self.session.execute(stmt)
        return new_item.scalar()

    async def update_by_id(self, item_id: int, item: BaseModel) -> T | None:
        stmt = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(**item.model_dump())
            .returning(self.model)
        )
        new_item = await self.session.execute(stmt)
        return new_item.scalar()

    async def delete_by_id(self, item_id: int) -> T | None:
        stmt = delete(self.model).where(self.model.id == item_id).returning(self.model)
        item = await self.session.execute(stmt)
        return item.scalar()
