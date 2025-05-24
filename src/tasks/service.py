from src.auth.exceptions import AccessDenied
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

            result = [TaskFromDb.model_validate(task) for task in tasks]
            return result

    async def create(self, new_task: CreateTask, user: Payload) -> TaskFromDb:
        async with self.uow as uow:
            task_to_db = CreateTaskToDb(**new_task.model_dump(), creator_id=user.id)
            task = await uow.tasks.create(task_to_db)
            await uow.commit()

            await uow.websocket.broadcast(
                f"User {user.username} has created task - {task.name}: {task.description}"
            )

            return TaskFromDb.model_validate(task)

    async def get_by_id(self, task_id: int):
        async with self.uow as uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise TaskNotFound
            return TaskFromDb.model_validate(task)

    async def update(self, task_id: int, task_to_update: CreateTask, user: Payload) -> TaskFromDb:
        async with self.uow as uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise TaskNotFound

            if task.creator_id != user.id:
                raise AccessDenied

            updated_task = await uow.tasks.update_by_id(task_id, task_to_update)
            await uow.commit()

            await uow.websocket.broadcast(
                f"User {user.username} has updated task - {updated_task.name}: {task.description}"
            )

            return TaskFromDb.model_validate(updated_task)

    async def delete(self, task_id: int, user: Payload):
        async with self.uow as uow:
            task = await uow.tasks.get_by_id(task_id)
            if not task:
                raise TaskNotFound

            if task.creator_id != user.id:
                raise AccessDenied

            deleted_task = await uow.tasks.delete_by_id(task_id)
            await uow.commit()

            await uow.websocket.broadcast(
                f"User {user.username} has deleted task - {deleted_task.name}"
            )

            return TaskFromDb.model_validate(deleted_task)
