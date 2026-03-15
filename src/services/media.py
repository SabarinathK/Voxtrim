import os

from moviepy import CompositeVideoClip, VideoFileClip
from moviepy.video.VideoClip import TextClip

from src.config import UPLOAD_DIR


def video_to_audio(video_path: str) -> str:
    audio_path = video_path.replace(".mp4", ".mp3")

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

    return audio_path


def add_subtitles(video_path: str, segments: list[dict]) -> str:
    video = VideoFileClip(video_path)
    subtitle_clips = []

    for seg in segments:
        txt_clip = TextClip(
            text=seg["text"],
            font_size=30,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(video.w * 0.6), None),
        )

        txt_clip = txt_clip.with_start(seg["start"]).with_end(seg["end"])
        txt_clip = txt_clip.with_position(("center", video.h * 0.75))
        subtitle_clips.append(txt_clip)

    final = CompositeVideoClip([video] + subtitle_clips)
    output = os.path.join(UPLOAD_DIR, "subtitled_video.mp4")
    final.write_videofile(output, codec="libx264", audio_codec="aac")

    video.close()
    final.close()

    return output

