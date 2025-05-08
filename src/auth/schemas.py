from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.tasks.schemas import TaskToUser


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    fullname: str | None = Field(default=None, max_length=100)
    age: int | None = Field(default=None, ge=18, le=99)


class CreateUser(BaseUser):
    password: str = Field(min_length=4, max_length=100)


class UserFromDb(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserFromDbWithTasks(UserFromDb):
    tasks: list[TaskToUser] = []


class UserLogin(BaseModel):
    username: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class Payload(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
