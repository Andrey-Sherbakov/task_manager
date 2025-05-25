# Task Manager
Task manager - FastAPI приложение для управления задачами с поддержкой отслеживания 
изменений в режиме реального времени при помощи WebSocket.
---

## Особенности
- Регистрация и аутентификация пользователей при помощи **JWT** токенов (refresh и access)
- Функционал создания, изменения, удаления и чтения для задач и пользователей
- Отслеживание изменений задач в режиме реального времени при помощи **WebSocket**
- Для работы с данными используется:
  * База — **PostgreSQL**
  * ORM — **SQLAlchemy**
  * Валидация — **Pydantic**
- Приложение полностью асинхронное:
  * бэкенд фреймворк — **FastAPI**
  * драйвер для базы данных — **asyncpg**
  * тесты — асинхронный **Pytest**
- Контейнеризация с помощью Docker для быстрого и удобного развертывания
---

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
5. Перейти на http://127.0.0.1:8000/docs#/
  
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
    alembic upgrade head
    ```
6. Запустить приложение:
    ```shell
    uvicorn src.main:app --reload
    ```
7. Перейти на http://127.0.0.1:8000/docs#/
---

## Тестирование с помощью Pytest
1. Перейти в главную директорию приложения
2. Запустить тесты:
    ```shell
    poetry run pytest
    ```