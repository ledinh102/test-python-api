from fastapi import APIRouter, File, UploadFile, HTTPException
from src.config.db import prismaConnection
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/translate/upload", tags=["translate"])
async def upload_video(video: UploadFile = File(...)):
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    # Save the uploaded video file
    file_path = f"{UPLOAD_DIR}/{video.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await video.read())

    return {"filename": video.filename}
