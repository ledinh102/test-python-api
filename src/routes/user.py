from fastapi import APIRouter, HTTPException
from src.config.db import prismaConnection

router = APIRouter()


@router.get("/users", tags=["users"])
async def list_users():
    try:
        users = await prismaConnection.prisma.user.find_many()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{email}", tags=["users"])
async def getUsers(email: str):
    try:
        response = await prismaConnection.prisma.user.find_many(
            where={"email": {"contains": email}}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/users/{text}", tags=["users"])
async def getUsersByNameOrEmail(id: str, text: str):
    try:
        response = await prismaConnection.prisma.user.find_many(
            where={
                "OR": [
                    {"name": {"contains": text, "mode": "insensitive"}},
                    {"email": {"contains": text, "mode": "insensitive"}},
                ],
                "id": {"not_in": [id]},
            },
            take=5,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/users", tags=["users"])
async def getUsersExcludeCurrentUser(id: str):
    try:
        response = await prismaConnection.prisma.user.find_many(
            where={"id": {"not_in": [id]}}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
