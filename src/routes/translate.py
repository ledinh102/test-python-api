import os
from fastapi import APIRouter, File, UploadFile, HTTPException
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

    # Convert WebM to MP4
    input_file = file_path
    output_file = f"{UPLOAD_DIR}/{Path(file_path).stem}.mp4"
    try:
        print(f"ffmpeg -i {input_file} {output_file} -y")
        os.system(f"ffmpeg -i {input_file} {output_file} -y")
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")

    return {"filename": video.filename, "converted_filename": Path(output_file).name}
