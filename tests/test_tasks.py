from httpx import AsyncClient

from src.auth.dependencies import get_authorize
from src.main import app
from src.tasks.schemas import TaskFromDb
from tests.conftest import fake_get_authorize

app.dependency_overrides[get_authorize] = fake_get_authorize

TEST_TASK: TaskFromDb


async def test_create_task(ac: AsyncClient):
    global TEST_TASK

    json = {
        "name": "test task",
        "description": "about test task",
    }
    response = await ac.post("/tasks/", json=json)

    assert response.status_code == 201

    response_json = response.json()
    for k, v in json.items():
        assert v == response_json[k]

    TEST_TASK = TaskFromDb.model_validate(response_json)


async def test_get_task(ac: AsyncClient):
    task_id = TEST_TASK.id
    response = await ac.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    response_model = TaskFromDb.model_validate(response.json())
    assert TEST_TASK == response_model


async def test_get_all_tasks(ac: AsyncClient):
    response = await ac.get("/tasks/")

    assert response.status_code == 200

    response_list = []
    for task in response.json():
        response_list.append(TaskFromDb.model_validate(task))
    assert response_list == [TEST_TASK]


async def test_update_task(ac: AsyncClient):
    global TEST_TASK

    task_id = TEST_TASK.id
    json = {
        "name": "updated test task",
        "description": "about updated test task",
    }

    response = await ac.put(f"/tasks/{task_id}", json=json)

    assert response.status_code == 200

    response_json = response.json()
    for k, v in json.items():
        assert v == response_json[k]

    TEST_TASK = TaskFromDb.model_validate(response_json)


async def test_delete_task(ac: AsyncClient):
    task_id = TEST_TASK.id
    response = await ac.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    response_model = TaskFromDb.model_validate(response.json())
    assert response_model == TEST_TASK

    all_tasks = await ac.get("/tasks/")
    assert all_tasks.json() == {"detail": "There is no tasks active"}
