import datetime

from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    name: str
    description: str | None = None


class TaskFromDb(CreateTask):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: datetime.datetime
