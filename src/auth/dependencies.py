from typing import Annotated

from fastapi import Depends, Request, Response

from src.auth.schemas import Payload
from src.auth.service import UserService
from src.core.dependencies import UOWDep


async def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_authorize(
    user_service: UserServiceDep, request: Request, response: Response
) -> Payload:
    return await user_service.authorize(request, response)


AuthorizeDep = Annotated[Payload, Depends(get_authorize)]
