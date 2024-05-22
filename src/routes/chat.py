from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.config.db import prismaConnection
from src.config.connectionManager import manager
from utils import getDifference
import json

router = APIRouter()


# @router.websocket("/chat/{userId}")
# async def websocket_endpoint(websocket: WebSocket, userId: str):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(data)
#             message = json.loads(data)
#             if message["senderId"] != userId:
#                 await manager.send_personal_message(data, websocket)
#             await manager.broadcast(data)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         # await manager.broadcast(f"Client #{userId} left the chat")
@router.websocket("/chat/{userId}")
async def websocket_endpoint(websocket: WebSocket, userId: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
