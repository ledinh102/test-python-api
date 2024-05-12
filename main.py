from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from utils import getDifference
import json
from decouple import config
from src.config.db import prismaConnection
from src.routes import user, videoCall, chat, conversation, message, translate


def init():
    app = FastAPI(title="DnD Translate", description="DnD Translate", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        print("Start Server")
        await prismaConnection.connect()

    @app.on_event("shutdown")
    async def shutdown():
        print("Stop Server")
        await prismaConnection.disconnect()

    @app.get("/")
    async def home():
        return "Hello World"

    app.include_router(user.router)
    app.include_router(videoCall.router)
    app.include_router(chat.router)
    app.include_router(conversation.router)
    app.include_router(message.router)
    app.include_router(translate.router)
    return app


app = init()
