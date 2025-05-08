from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.websocket.utils import websocket_manager

router = APIRouter(prefix="/websocket", tags=["websocket"])


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    websocket_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast(f"Message from {username}: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


@router.post("/send_message")
async def send_message(message: str):
    await websocket_manager.broadcast(message)
