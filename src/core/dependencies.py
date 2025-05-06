from typing import Annotated

from fastapi import Depends

from src.core.db import async_session_maker
from src.core.utils import IUnitOfWork, AsyncUnitOfWork


async def get_async_uow() -> AsyncUnitOfWork:
    return AsyncUnitOfWork(async_session_maker)


UOWDep = Annotated[IUnitOfWork, Depends(get_async_uow)]
