from fastapi import APIRouter, status, Request, Response

from src.auth.dependencies import UserServiceDep, AuthorizeDep
from src.auth.schemas import CreateUser, UserFromDb, UserFromDbWithTasks, UserLogin, Tokens, Payload

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserFromDb,
)
async def create_user(new_user: CreateUser, service: UserServiceDep) -> UserFromDb:
    user = await service.create(new_user)
    return user


@router.get("/profile", response_model=UserFromDbWithTasks)
async def get_user(service: UserServiceDep, user: AuthorizeDep) -> UserFromDbWithTasks:
    user = await service.get_with_tasks(user)
    return user


@router.post("/login", response_model=Tokens)
async def login(response: Response, user_login: UserLogin, service: UserServiceDep) -> Tokens:
    tokens = await service.authenticate(response, user_login)
    return tokens


@router.get("/authorize", response_model=Payload)
async def authorize(request: Request, response: Response, service: UserServiceDep) -> Payload:
    """
    test endpoint
    todo: delete later
    """
    payload = await service.authorize(request, response)
    return payload
