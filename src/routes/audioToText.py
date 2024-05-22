# # from fastapi import APIRouter, File, UploadFile, HTTPException
# # from fastapi.responses import JSONResponse
# # from tempfile import NamedTemporaryFile
# # import os
# # import speech_recognition as sr
# # from pydub import AudioSegment

# # router = APIRouter()
# # r = sr.Recognizer()


# # @router.post("/audio-to-text/", tags=["audio-to-text"])
# # async def upload_file(file: UploadFile = File(...)):
# #     if not (file.filename.endswith(".wav") or file.filename.endswith(".mp3")):
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Invalid file format. Only .wav and .mp3 files are allowed.",
# #         )

# #     try:
# #         if file.filename.endswith(".mp3"):
# #             with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3_file:
# #                 temp_mp3_file.write(await file.read())
# #                 temp_mp3_file_path = temp_mp3_file.name

# #             # Convert MP3 to WAV
# #             audio = AudioSegment.from_mp3(temp_mp3_file_path)
# #             with NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
# #                 audio.export(temp_wav_file.name, format="wav")
# #                 temp_file_path = temp_wav_file.name

# #             # Remove the temporary MP3 file
# #             os.remove(temp_mp3_file_path)
# #         else:
# #             with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
# #                 temp_file.write(await file.read())
# #                 temp_file_path = temp_file.name

# #         try:
# #             with sr.AudioFile(temp_file_path) as source:
# #                 audio_data = r.record(source)
# #                 text = r.recognize_google(audio_data)
# #                 return JSONResponse(content={"text": text})
# #         except sr.UnknownValueError:
# #             raise HTTPException(
# #                 status_code=400,
# #                 detail="Speech recognition could not understand audio",
# #             )
# #         except sr.RequestError as e:
# #             raise HTTPException(
# #                 status_code=500,
# #                 detail=f"Could not request results; {e}",
# #             )
# #         finally:
# #             if os.path.exists(temp_file_path):
# #                 os.remove(temp_file_path)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, File, UploadFile
import subprocess
import os
from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError

router = APIRouter()


@router.post("/audio-to-text/", tags=["audio-to-text"])
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    webm_filename = "input.webm"
    wav_filename = "output.wav"
    with open(webm_filename, "wb") as buffer:
        buffer.write(await file.read())

    # Convert webm to wav using ffmpeg
    convert_command = f"ffmpeg -i {webm_filename} {wav_filename} -y"
    subprocess.run(convert_command, shell=True)

    # Recognize text from the wav file
    recognizer = Recognizer()
    text = ""
    try:
        with AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except UnknownValueError:
        text = "Could not understand audio"
    except RequestError as e:
        text = f"Could not request results; {e}"

    # Clean up the files
    os.remove(webm_filename)
    os.remove(wav_filename)

    return {"text": text}
