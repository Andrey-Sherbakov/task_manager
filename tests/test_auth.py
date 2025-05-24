from httpx import AsyncClient

from src.auth.schemas import UserFromDb, Tokens, UserWithTasks

TEST_USER = UserFromDb


async def test_create_user(ac: AsyncClient):
    global TEST_USER

    json = {
        "username": "test_name",
        "password": "test_password",
        "email": "test@email.com",
    }
    response = await ac.post("/auth/register", json=json)

    assert response.status_code == 201

    TEST_USER = UserFromDb.model_validate(response.json())
    assert json["username"] == TEST_USER.username
    assert json["email"] == TEST_USER.email


async def test_login(ac: AsyncClient):
    json = {"username": TEST_USER.username, "password": "test_password"}
    response = await ac.post("/auth/login", json=json)

    assert response.status_code == 200

    tokens = Tokens.model_validate(response.json())
    assert tokens.access_token
    assert tokens.refresh_token


async def test_get_user(ac: AsyncClient):
    response = await ac.get("/auth/profile")

    assert response.status_code == 200

    user_with_tasks = UserWithTasks.model_validate(response.json())
    assert user_with_tasks.tasks == []

    user = UserFromDb.model_validate(response.json())
    assert user == TEST_USER
