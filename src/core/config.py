from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TokenType(Enum):
    access = "access"
    refresh = "refresh"


class Settings(BaseSettings):
    # postgres params
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # test postgres params
    TEST_USER: str
    TEST_PASS: str
    TEST_HOST: str
    TEST_PORT: str
    TEST_NAME: str

    # JWT params
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION: int
    REFRESH_TOKEN_EXPIRATION: int

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_USER}:{self.TEST_PASS}@{self.TEST_HOST}:"
            f"{self.TEST_PORT}/{self.TEST_NAME}"
        )

    def get_token_expiration(self, token_type: TokenType) -> int:
        if token_type == TokenType.refresh:
            return self.REFRESH_TOKEN_EXPIRATION
        else:
            return self.ACCESS_TOKEN_EXPIRATION


settings = Settings()
