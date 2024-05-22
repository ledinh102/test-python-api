from fastapi import APIRouter, HTTPException
from src.config.db import prismaConnection
from pydantic import BaseModel
from typing import List

router = APIRouter()


class UserIdList(BaseModel):
    ids: List[str]


class EditUser(BaseModel):
    name: str
    email: str
    image: str
    role: str


class CreateUser(EditUser):
    password: str


@router.get("/users", tags=["users"])
async def list_users():
    try:
        users = await prismaConnection.prisma.user.find_many(
            order={"updatedAt": "desc"}
        )
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/id/{userId}", tags=["users"])
async def get_user_by_id(userId: str):
    try:
        response = await prismaConnection.prisma.user.find_unique(where={"id": userId})
        if not response:
            raise HTTPException(status_code=404, detail="User not found")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{userId}/users/email/{email}", tags=["users"])
async def get_user_by_email(userId: str, email: str):
    try:
        response = await prismaConnection.prisma.user.find_many(
            where={"email": {"contains": email}, "id": {"not": userId}}, take=10
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/search/{id}/{text}", tags=["users"])
async def get_users_by_name_or_email(id: str, text: str):
    try:
        response = await prismaConnection.prisma.user.find_many(
            where={
                "OR": [
                    {"name": {"contains": text, "mode": "insensitive"}},
                    {"email": {"contains": text, "mode": "insensitive"}},
                ],
                "id": {"not": id},
            },
            take=5,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/multiple", tags=["users"])
async def create_users(users: List[CreateUser]):
    try:
        user_dicts = [user.dict() for user in users]
        # Use the create_many method with the list of dictionaries
        response = await prismaConnection.prisma.user.create_many(data=user_dicts)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users", tags=["users"])
async def create_user(user: CreateUser):
    try:
        response = await prismaConnection.prisma.user.create(
            data={
                "name": user.name,
                "email": user.email,
                "image": user.image,
                "password": user.password,
                "role": user.role,
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users", tags=["users"])
async def delete_users(user_ids: UserIdList):
    try:
        response = await prismaConnection.prisma.user.delete_many(
            where={"id": {"in": user_ids.ids}}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: str):
    try:
        response = await prismaConnection.prisma.user.delete(where={"id": id})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/users/{id}", tags=["users"])
async def update_user(id: str, user: EditUser):
    try:
        response = await prismaConnection.prisma.user.update(
            where={"id": id},
            data={
                "name": user.name,
                "email": user.email,
                "image": user.image,
                "role": user.role,
            },
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
