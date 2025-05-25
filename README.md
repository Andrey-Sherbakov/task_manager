# Task Manager
Task manager - FastAPI приложение для управления задачами с поддержкой отслеживания 
изменений в режиме реального времени при помощи WebSocket.
---

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
---

## Установка и запуск

- Клонировать репозиторий:
  ```shell
  git clone https://github.com/Andrey-Sherbakov/task_manager.git
  cd task_manager
  ```
- Изменить данные в файле .sample.env на свои и переименовать его в .env

### 1. При помощи Docker
- Запустить docker compose:
  ```shell
  docker compose up --build
  ```
- Применить миграции:
  ```shell
  docker compose exec app alembic upgrade head
  ```
- Перейти на http://127.0.0.1:8000/docs#/
  
### 2. При помощи Poetry
- Установить зависимости:
  ```shell
  poetry install
  ```
- Применить миграции:
  ```shell
  alembic upgrade head
  ```
- Запустить приложение:
  ```shell
  uvicorn src.main:app --reload
  ```
- Перейти на http://127.0.0.1:8000/docs#/