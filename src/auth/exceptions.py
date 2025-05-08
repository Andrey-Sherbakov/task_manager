from fastapi import HTTPException
from starlette import status


class UserAlreadyExists(HTTPException):
    def __init__(
        self,
        detail: str = "User with this username or email already exists",
        status_code: int = status.HTTP_409_CONFLICT,
    ):
        super().__init__(detail=detail, status_code=status_code)


class UserNotFound(HTTPException):
    def __init__(
        self,
        detail: str = "There is no user with requested username",
        status_code: status = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(detail=detail, status_code=status_code)


class AuthenticationError(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid username or password",
        status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(detail=detail, status_code=status_code)


class AuthorizationError(HTTPException):
    def __init__(
        self,
        detail: str = "Authorization required",
        status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(detail=detail, status_code=status_code)


class TokenExpired(HTTPException):
    def __init__(
        self,
        detail: str = "Token expired",
        status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(detail=detail, status_code=status_code)


class TokenError(HTTPException):
    def __init__(
        self,
        detail: str = "Token validation error",
        status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(detail=detail, status_code=status_code)
