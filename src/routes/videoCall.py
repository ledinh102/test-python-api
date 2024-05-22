from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.config.db import prismaConnection
from src.config.connectionManager import manager
from utils import getDifference

router = APIRouter()


@router.websocket("/video-call/{userId}")
async def speakToSign(websocket: WebSocket):
    await manager.connect(websocket)
    oldData = ""
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            diff = getDifference(oldData, data)
            if diff:
                print(oldData, data)
                print(diff)
                await manager.broadcast(diff)
                oldData = data

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
