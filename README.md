# Task Manager

Task manager - FastAPI приложение для управления задачами с поддержкой отслеживания 
изменений в режиме реального времени при помощи WebSocket.


## Особенности

- Регистрация и аутентификация пользователей при помощи **JWT** токенов (refresh и access)
- Функционал создания, изменения, удаления и чтения для задач и пользователей
- Отслеживание изменений задач в режиме реального времени при помощи **WebSocket**
- Для работы с данными используется:
  * База данных — **PostgreSQL**
  * ORM — **SQLAlchemy**
  * Валидация данных — **Pydantic**
- Приложение полностью асинхронное:
  * бэкенд фреймворк — **FastAPI**
  * драйвер для базы данных — **asyncpg**
  * тесты — асинхронный **Pytest**
- Контейнеризация с помощью Docker для быстрого и удобного развертывания


## Установка и запуск

### Docker
1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Andrey-Sherbakov/task_manager.git
    cd task_manager
    ```
2. Изменить данные в файле .sample.env на свои и переименовать его в .env
3. Запустить docker compose:
    ```shell
    docker compose up --build
    ```
4. Применить миграции:
    ```shell
    docker compose exec app alembic upgrade head
    ```
  
### Poetry
1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Andrey-Sherbakov/task_manager.git
    cd task_manager
    ```
2. Изменить данные в файле .sample.env на свои и переименовать его в .env
3. Установить [Poetry](https://python-poetry.org/docs/#installation)
4. Установить зависимости:
    ```shell
    poetry install
    ```
5. Применить миграции:
    ```shell
    poetry run alembic upgrade head
    ```
6. Запустить приложение:
    ```shell
    poetry run uvicorn src.main:app --reload
    ```

## API
После запуска документация доступна по адресу http://127.0.0.1:8000/docs/
![image](https://drive.google.com/uc?id=1LLZqQkXmznoMut_GB49JIrFXSNIjgD64)

## Тестирование с помощью Pytest
1. Перейти в главную директорию приложения
2. Запустить тесты:
    ```shell
    poetry run pytest

## Структура проекта
```
.
├── alembic
│     ├── versions
│     │     └── ...
│     ├── README
│     ├── env.py
│     └── script.py.mako
├── src
│     ├── auth
│     │     ├── dependencies.py
│     │     ├── exceptions.py
│     │     ├── models.py
│     │     ├── repository.py
│     │     ├── router.py
│     │     ├── schemas.py
│     │     ├── security.py
│     │     └── service.py
│     ├── core
│     │     ├── config.py
│     │     ├── db.py
│     │     ├── dependencies.py
│     │     ├── repository.py
│     │     └── utils.py
│     ├── tasks
│     │     ├── dependencies.py
│     │     ├── exceptions.py
│     │     ├── models.py
│     │     ├── repository.py
│     │     ├── router.py
│     │     ├── schemas.py
│     │     └── service.py
│     ├── websocket
│     │     ├── router.py
│     │     └── utils.py
│     ├── Dockerfile
│     └── main.py
├── tests
│     ├── conftest.py
│     ├── test_auth.py
│     └── test_tasks.py
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── requirements.txt

```