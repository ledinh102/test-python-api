from fastapi import APIRouter, File, UploadFile, HTTPException
import os
from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError
from pathlib import Path
import asyncio
import subprocess
import aiofiles


router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/audioToText", tags=["audioToText"])
async def upload_video(video: UploadFile = File(...)):
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    # Save the uploaded video file
    file_path = f"{UPLOAD_DIR}/{video.filename}"
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await video.read()  # async read
        await out_file.write(content)  # async write

    # Convert WebM to MP4
    input_file = file_path
    output_file = f"{UPLOAD_DIR}/{Path(file_path).stem}.wav"
    try:
        command = f"ffmpeg -i {input_file} {output_file} -y"
        subprocess.run(command, shell=True, check=True)

        recognizer = Recognizer()
        text = ""
        error = ""
        try:
            with AudioFile(output_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
        except UnknownValueError:
            error = "Could not understand audio"
        except RequestError as e:
            error = f"Could not request results; {e}"

        # Clean up the files
        os.remove(input_file)
        os.remove(output_file)

        return {"text": text, "error": error}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")
