from fastapi import Request, Response
from sqlalchemy.exc import IntegrityError

from src.auth import security
from src.auth.exceptions import (
    UserAlreadyExists,
    UserNotFound,
    AuthenticationError,
    TokenExpired,
    AuthorizationError,
)
from src.auth.schemas import CreateUser, UserFromDb, UserFromDbWithTasks, UserLogin, Payload, Tokens
from src.core.config import TokenType
from src.core.utils import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create(self, new_user: CreateUser) -> UserFromDb:
        async with self.uow as uow:
            new_user.password = security.hash_password(new_user.password)
            try:
                user = await uow.users.create(new_user)
                await uow.commit()
                return UserFromDb.model_validate(user)
            except IntegrityError:
                raise UserAlreadyExists

    async def get_with_tasks(self, user: Payload) -> UserFromDbWithTasks:
        async with self.uow as uow:
            user = await uow.users.get_by_username_with_tasks(user.username)
            if not user:
                raise UserNotFound
            return UserFromDbWithTasks.model_validate(user)

    async def authenticate(self, response: Response, user_login: UserLogin) -> Tokens:
        async with self.uow as uow:
            user = await uow.users.get_by_username(user_login.username)
            if not user or not security.verify_password(
                password=user_login.password, hashed_password=str(user.password)
            ):
                raise AuthenticationError

            tokens = security.create_tokens(Payload.model_validate(user))

            security.set_tokens_to_cookies(response, tokens)

            return tokens

    async def authorize(self, request: Request, response: Response) -> Payload:
        tokens = security.get_tokens_from_cookies(request)

        try:
            payload = security.verify_token(tokens.access_token, TokenType.access)
        except TokenExpired:
            tokens = await self.update_tokens(request, response)
            payload = security.verify_token(tokens.access_token, TokenType.access)

        return payload

    @staticmethod
    async def update_tokens(request: Request, response: Response) -> Tokens:
        tokens = security.get_tokens_from_cookies(request)

        try:
            payload = security.verify_token(tokens.refresh_token, TokenType.refresh)
            tokens = security.create_tokens(payload)
            security.set_tokens_to_cookies(response, tokens)

            print("tokens_updated")

            return tokens

        except TokenExpired:
            raise AuthorizationError
