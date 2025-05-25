from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.auth.dependencies import get_authorize
from src.auth.models import User
from src.auth.schemas import Payload
from src.core.config import settings
from src.core.db import Base
from src.core.utils import AsyncUnitOfWork
from src.main import app

engine_test = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
test_async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test

FAKE_USER = {
    "username": "user_test",
    "password": "password_test",
    "hashed_password": "$2b$12$nsigdvEFxBJ6oSmBWDSvAePyQS1y0evPr6BIop.d4Ovp9uEr//S8C",
    "email": "test@user.com",
}


@pytest.fixture(autouse=True, scope="module")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_async_session_maker() as session:
        test_user = User(
            username=FAKE_USER["username"],
            password=FAKE_USER["hashed_password"],
            email=FAKE_USER["email"],
        )
        session.add(test_user)
        await session.commit()

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class TestAsyncUnitOfWork(AsyncUnitOfWork):
    def __init__(self):
        super().__init__()
        self._session_factory = test_async_session_maker


app.dependency_overrides[AsyncUnitOfWork] = TestAsyncUnitOfWork


async def fake_get_authorize():
    return Payload(id=1, username="user_test", email="test@user.com")


app.dependency_overrides[get_authorize] = fake_get_authorize


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
        yield ac
