from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.tasks.router import router as tasks_router
from src.websocket.router import router as ws_router

app = FastAPI()

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(ws_router)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to task manager!"}
