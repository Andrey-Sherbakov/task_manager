import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    name: str
    description: str | None = None


class TaskFromDb(CreateTask):
    id: int
    updated_at: datetime.datetime
