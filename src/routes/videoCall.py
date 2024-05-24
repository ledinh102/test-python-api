import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.config.connectionManager import manager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/video-call/{userId}/{userType}")
async def speakToSign(websocket: WebSocket, userType: str) -> None:
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if userType == "dd":
                await manager.broadcast_string(data)
            elif userType == "normal":
                await manager.broadcast_string(data)
            else:
                logger.error(f"Invalid user type: {userType}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.warning("WebSocket disconnected")
        # Add any cleanup code here
