from fastapi import APIRouter
from sqlalchemy import Sequence
from starlette import status

from src.core.db import SessionDep
from src.tasks.models import Task
from src.tasks.repository import TaskRepository
from src.tasks.schemas import CreateTask, TaskFromDb

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskFromDb])
async def get_all_tasks(session: SessionDep) -> Sequence[Task]:
    """todo get all tasks"""
    repo = TaskRepository(session)
    return await repo.get_all()


@router.get("/{task_id}")
async def get_task(task_id: int):
    """todo get task by id"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskFromDb)
async def create_task(task: CreateTask, session: SessionDep) -> Task:
    repo = TaskRepository(session)
    new_task: Task = await repo.create(task)
    await session.commit()
    return new_task


@router.put("/{task_id}")
async def update_task(task_id: int):
    """todo update task by id"""


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    """todo delete task by id"""
