from fastapi import APIRouter, HTTPException
from src.config.db import prismaConnection
from pydantic import BaseModel

router = APIRouter()


class CreateMessage(BaseModel):
    conversationId: str
    senderId: str
    content: str


@router.get("/{conversationId}/messages", tags=["messages"])
async def messageList(conversationId: str):
    if conversationId is None:
        raise ValueError("id is null")
    try:
        messageList = await prismaConnection.prisma.message.find_many(
            where={
                "conversationId": {"equals": conversationId},
            },
            order={"sentTime": "asc"},
            take=100,
        )
        if messageList is None:
            raise ValueError("conversationList is null")
        return messageList
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}") from e


@router.post("/messages", tags=["messages"])
async def createMessage(createMessage: CreateMessage):
    try:
        response = await prismaConnection.prisma.message.create(
            data={
                "conversationId": createMessage.conversationId,
                "senderId": createMessage.senderId,
                "content": createMessage.content,
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.delete("/messages/{id}", tags=["messages"])
async def deleteMessage(id: str):
    try:
        response = await prismaConnection.prisma.message.delete(where={"id": id})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
