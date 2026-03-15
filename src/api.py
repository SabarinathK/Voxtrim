import os

from fastapi import FastAPI, File, UploadFile

from src.config import UPLOAD_DIR
from src.services.media import add_subtitles, video_to_audio
from src.services.transcription import (
    build_word_groups,
    filter_segments,
    transcribe,
)


app = FastAPI()


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(video_path, "wb") as f:
        f.write(await file.read())

    audio_path = video_to_audio(video_path)
    transcript = transcribe(audio_path)
    clean_segments = filter_segments(transcript)
    subtitle_segments = build_word_groups(clean_segments)
    final_video = add_subtitles(video_path, subtitle_segments)

    return {"segments": subtitle_segments, "video": final_video}

