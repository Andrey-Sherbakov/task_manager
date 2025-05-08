import datetime

import jwt
from fastapi import Request, Response
from passlib.context import CryptContext

from src.auth.exceptions import TokenError, TokenExpired, AuthorizationError
from src.auth.schemas import Tokens, Payload
from src.core.config import settings, TokenType

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


def create_token(payload: Payload, token_type: TokenType) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=settings.get_token_expiration(token_type)
    )
    payload = payload.model_dump()
    payload.update({"exp": exp, "type": token_type.value})

    encoded_jwt = jwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def create_tokens(payload: Payload) -> Tokens:
    access_token = create_token(payload, TokenType.access)
    refresh_token = create_token(payload, TokenType.refresh)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


def verify_token(token: str, token_type: TokenType):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        if payload.get("type") != token_type.value:
            raise TokenError

        return Payload.model_validate(payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise TokenExpired
    except jwt.exceptions.InvalidTokenError:
        raise TokenError


def set_tokens_to_cookies(response: Response, tokens: Tokens):
    response.set_cookie("access_token", tokens.access_token, httponly=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    return response


def get_tokens_from_cookies(request: Request) -> Tokens:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        return Tokens(access_token=access_token, refresh_token=refresh_token)
    else:
        raise AuthorizationError
