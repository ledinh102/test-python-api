from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from src.config.db import prismaConnection
from pydantic import BaseModel
from src.config.connectionManager import manager
from typing import List

router = APIRouter()


@router.get("/{userId}/conversations", tags=["conversations"])
async def conversationList(userId: str):
    if userId is None:
        raise ValueError("id is null")
    try:
        conversationList = await prismaConnection.prisma.conversation.find_many(
            where={
                "OR": [{"user1Id": {"equals": userId}}, {"user2Id": {"equals": userId}}]
            },
            include={"Message": True, "user1": True, "user2": True},
        )
        if conversationList is None:
            raise ValueError("conversationList is null")
        return conversationList
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e


@router.get("/conversations/{id}", tags=["conversations"])
async def conversationList(id: str):
    if id is None:
        raise ValueError("id is null")
    try:
        conversation = await prismaConnection.prisma.conversation.find_unique(
            where={"id": id},
            include={"Message": True, "user1": True, "user2": True},
        )
        if conversation is None:
            raise ValueError("conversationList is null")
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e


@router.get("/sum-conversations-and-messages", tags=["conversations"])
async def get():
    try:
        countConversation = await prismaConnection.prisma.conversation.count()
        countMessage = await prismaConnection.prisma.message.count()
        return [
            {"label": "Conversations", "data": [countConversation]},
            {"label": "Messages", "data": [countMessage]},
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


class CreateConversation(BaseModel):
    user1Id: str
    user2Id: str


@router.post("/conversations", tags=["conversations"])
async def createConversation(createConversation: CreateConversation):
    try:
        # Tìm xem có cuộc trò chuyện nào tồn tại giữa hai người dùng
        print(createConversation)
        hadConversation = await prismaConnection.prisma.conversation.find_many(
            where={
                "OR": [
                    {
                        "user1Id": createConversation.user1Id,
                        "user2Id": createConversation.user2Id,
                    },
                    {
                        "user1Id": createConversation.user2Id,
                        "user2Id": createConversation.user1Id,
                    },
                ]
            }
        )

        if hadConversation.__len__() == 0:
            # Tạo cuộc trò chuyện mới nếu không có cuộc trò chuyện nào tồn tại
            conversation = await prismaConnection.prisma.conversation.create(
                data={
                    "user1Id": createConversation.user1Id,
                    "user2Id": createConversation.user2Id,
                },
            )
            return {
                "id": conversation.id,
                "user1Id": conversation.user1Id,
                "user2Id": conversation.user2Id,
                "status": "added",
            }
        else:
            # Trả về cuộc trò chuyện đã tồn tại
            return {
                "id": hadConversation[0].id,
                "user1Id": hadConversation[0].user1Id,
                "user2Id": hadConversation[0].user2Id,
                "status": "had",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
