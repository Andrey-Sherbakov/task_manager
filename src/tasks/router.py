from fastapi import APIRouter
from starlette import status

from src.auth.dependencies import AuthorizeDep
from src.tasks.dependencies import TaskServiceDep
from src.tasks.schemas import CreateTask, TaskFromDb

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskFromDb])
async def get_all_tasks(service: TaskServiceDep) -> list[TaskFromDb]:
    return await service.get_all()


@router.get("/{task_id}", response_model=TaskFromDb)
async def get_task(task_id: int, service: TaskServiceDep) -> TaskFromDb:
    return await service.get_by_id(task_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskFromDb)
async def create_task(task: CreateTask, service: TaskServiceDep, user: AuthorizeDep) -> TaskFromDb:
    return await service.create(task, user)


@router.put("/{task_id}", response_model=TaskFromDb)
async def update_task(
    task_id: int, updated_task: CreateTask, service: TaskServiceDep, user: AuthorizeDep
) -> TaskFromDb:
    return await service.update(task_id, updated_task, user)


@router.delete("/{task_id}", response_model=TaskFromDb)
async def delete_task(task_id: int, service: TaskServiceDep, user: AuthorizeDep) -> TaskFromDb:
    return await service.delete(task_id, user)
