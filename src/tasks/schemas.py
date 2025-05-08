import datetime

from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    name: str
    description: str | None = None


class CreateTaskToDb(CreateTask):
    creator_id: int


class TaskToUser(CreateTask):
    id: int
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class TaskFromDb(TaskToUser):
    creator_id: int
