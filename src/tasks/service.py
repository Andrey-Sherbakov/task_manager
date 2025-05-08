from src.auth.schemas import Payload
from src.core.utils import IUnitOfWork
from src.tasks.exceptions import TasksNotFound, TaskNotFound
from src.tasks.schemas import TaskFromDb, CreateTask, CreateTaskToDb


class TaskService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def get_all(self) -> list[TaskFromDb]:
        async with self.uow as uow:
            tasks = await uow.tasks.get_all()
            if not tasks:
                raise TasksNotFound
            result = []
            for task in tasks:
                result.append(TaskFromDb.model_validate(task))
            return result

    async def create(self, new_task: CreateTask, user: Payload):
        async with self.uow as uow:
            task_to_db = CreateTaskToDb(**new_task.model_dump(), creator_id=user.id)
            task = await uow.tasks.create(task_to_db)
            await uow.commit()
            return TaskFromDb.model_validate(task)

    async def get_by_id(self, task_id: int):
        async with self.uow as uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise TaskNotFound
            return TaskFromDb.model_validate(task)

    async def update(self, task_id: int, updated_task: CreateTask) -> TaskFromDb:
        async with self.uow as uow:
            task = await uow.tasks.update_by_id(task_id, updated_task)
            if not task:
                raise TaskNotFound
            await uow.commit()
            return TaskFromDb.model_validate(task)

    async def delete(self, task_id: int):
        async with self.uow as uow:
            task = await uow.tasks.delete_by_id(task_id)
            if not task:
                raise TaskNotFound
            await uow.commit()
            return TaskFromDb.model_validate(task)
