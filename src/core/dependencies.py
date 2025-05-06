from typing import Annotated

from fastapi import Depends

from src.core.utils import IUnitOfWork, AsyncUnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(AsyncUnitOfWork)]
