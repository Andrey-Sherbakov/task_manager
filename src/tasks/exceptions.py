from fastapi import HTTPException
from starlette import status


class TasksNotFound(HTTPException):
    def __init__(
        self,
        detail: str = "There is no tasks active",
        status_code: status = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(detail=detail, status_code=status_code)


class TaskNotFound(HTTPException):
    def __init__(
        self,
        detail: str = "There is no task with requested id",
        status_code: status = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(detail=detail, status_code=status_code)
