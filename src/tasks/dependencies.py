from typing import Annotated

from fastapi.params import Depends

from src.core.dependencies import UOWDep
from src.tasks.service import TaskService


async def get_task_service(uow: UOWDep) -> TaskService:
    return TaskService(uow)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
