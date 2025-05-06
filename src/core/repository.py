from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import select, Sequence, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import Base


class IRepository(ABC):
    @abstractmethod
    async def get_by_id(self, item_id: int) -> Base | None: ...

    @abstractmethod
    async def get_all(self) -> Sequence[Base]: ...

    @abstractmethod
    async def create(self, item: BaseModel) -> Base: ...

    @abstractmethod
    async def update_by_id(self, item_id: int, item: BaseModel) -> Base | None: ...

    @abstractmethod
    async def delete_by_id(self, item_id: int) -> Base | None: ...


class SQLAlchemyORMRepository(IRepository):
    model: Base | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: int) -> model:
        stmt = select(self.model).where(self.model.id == item_id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[model]:
        stmt = select(self.model)
        items = await self.session.scalars(stmt)
        return items.all()

    async def create(self, item: BaseModel) -> model:
        stmt = insert(self.model).values(**item.model_dump()).returning(self.model)
        new_item = await self.session.execute(stmt)
        return new_item.scalar()

    async def update_by_id(self, item_id: int, item: BaseModel) -> model:
        stmt = update(self.model).where(self.model.id == item_id).values(**item.model_dump())
        new_item = await self.session.execute(stmt)
        return new_item.scalar()

    async def delete_by_id(self, item_id: int) -> model:
        stmt = delete(self.model).where(self.model.id == item_id)
        item = await self.session.execute(stmt)
        return item.scalar()
