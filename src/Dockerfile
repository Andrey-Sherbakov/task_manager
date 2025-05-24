FROM python:3.13-slim
RUN groupadd -r task_group && useradd -r -g task_group task_user

ENV HOME=/home/task_manager \
    PYTHONPATH="$PYTHONPATH:/home/task_manager/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR $HOME

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY src src
COPY alembic alembic
COPY alembic.ini .

USER task_user
