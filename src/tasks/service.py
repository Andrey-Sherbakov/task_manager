from sqlalchemy import Sequence

from src.core.utils import IUnitOfWork
from src.tasks.exceptions import TasksNotFound
from src.tasks.models import Task


class TaskService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def get_all_tasks(self) -> Sequence[Task]:
        async with self.uow as uow:
            tasks = uow.tasks.get_all()
            if not tasks:
                raise TasksNotFound()
            return tasks
