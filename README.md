# AI Video Editor API

A FastAPI service that accepts an uploaded video, extracts audio, transcribes speech with Groq Whisper, removes simple filler-only segments, generates subtitle timing groups, and renders a subtitled output video with MoviePy.

## Overview

This project provides a single HTTP API for subtitle generation on uploaded videos. The current pipeline is:

1. Upload an MP4 video to the API.
2. Extract the audio track as MP3.
3. Transcribe the audio using Groq's `whisper-large-v3`.
4. Remove transcript segments that are only filler words such as `um`, `uh`, `like`, and `you know`.
5. Split transcript text into subtitle chunks.
6. Burn subtitles into the source video.
7. Return the generated subtitle segments and output video path.

## Features

- FastAPI-based upload endpoint
- Groq Whisper transcription integration
- Basic filler-only segment filtering
- Subtitle chunk generation based on fixed word groups
- Burned-in subtitles rendered with MoviePy
- Modular source layout under `src/`

## Project Structure

```text
ai-video-editor/
|-- main.py
|-- README.md
|-- .gitignore
|-- .env
|-- uploads/
`-- src/
    |-- __init__.py
    |-- api.py
    |-- config.py
    `-- services/
        |-- __init__.py
        |-- media.py
        `-- transcription.py
```

## Tech Stack

- Python 3.10+
- FastAPI
- Groq Python SDK
- MoviePy
- python-dotenv

## Requirements

Before running the service, make sure you have:

- Python 3.10 or newer
- `ffmpeg` installed and available on your system `PATH`
- A valid Groq API key with access to audio transcription

MoviePy depends on `ffmpeg` for media processing. If `ffmpeg` is missing, audio extraction and video rendering will fail.

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Installation

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install project dependencies.

```powershell
pip install fastapi uvicorn moviepy groq python-dotenv python-multipart
```

3. Verify `ffmpeg` is installed.

```powershell
ffmpeg -version
```

## Running the API

Start the FastAPI app with Uvicorn:

```powershell
uvicorn main:app --reload
```

By default, the API will be available at:

```text
http://127.0.0.1:8000
```

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Reference

### `POST /upload`

Uploads a video, generates subtitles, and renders a new subtitled video.

#### Request

- Content type: `multipart/form-data`
- Form field: `file`

Example with `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.mp4"
```

#### Success Response

```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 1.8,
      "text": "Hello and welcome to"
    }
  ],
  "video": "uploads/subtitled_video.mp4"
}
```

#### Response Fields

- `segments`: Subtitle timing blocks generated from the transcript
- `video`: Relative path to the rendered output file

## Architecture

### Entry Point

- `main.py` exposes the ASGI app for Uvicorn and deployment tooling.

### API Layer

- `src/api.py` defines the FastAPI app and the `/upload` endpoint.

### Configuration Layer

- `src/config.py` loads environment variables, initializes the Groq client, defines shared constants, and ensures the upload directory exists.

### Service Layer

- `src/services/media.py` handles audio extraction and subtitle rendering.
- `src/services/transcription.py` handles transcription, transcript cleanup, and subtitle chunk generation.

## Operational Notes

- Uploaded videos are stored in `uploads/`.
- The generated output filename is currently fixed as `uploads/subtitled_video.mp4`.
- Audio is extracted by replacing the `.mp4` extension with `.mp3`.
- Subtitle chunking currently groups text by a fixed number of words.
- Filler filtering only removes segments whose full text exactly matches a configured filler phrase.

## Known Limitations

- The service currently assumes MP4 input.
- Output filenames are not unique, so concurrent requests can overwrite previous results.
- There is no cleanup job for uploaded or generated media.
- There is no request authentication or authorization.
- There is no structured logging, retries, rate limiting, or background job queue.
- Errors from transcription and video processing are not yet wrapped in production-grade exception handling.
- Large uploads are processed synchronously and may block worker capacity.

## Production Recommendations

For real production deployment, consider the following improvements:

- Add unique file naming and per-request working directories.
- Add validation for file type, size, and media duration.
- Move heavy video processing to a background worker such as Celery, RQ, or Dramatiq.
- Add structured logging and centralized error reporting.
- Add health check endpoints and observability metrics.
- Add automated tests for upload flow, transcription processing, and subtitle generation.
- Add Docker support and pinned dependency management.
- Add authentication if the API is exposed outside a trusted environment.
- Store output assets in object storage instead of local disk for multi-instance deployments.

## Development Notes

If you want to extend the subtitle pipeline, the most likely change points are:

- `src/config.py` for shared constants such as filler words and subtitle group size
- `src/services/transcription.py` for text cleanup and subtitle segment generation
- `src/services/media.py` for subtitle styling, positioning, and render behavior

## Troubleshooting

### `ModuleNotFoundError: No module named 'fastapi'`

Install the required dependencies in your active virtual environment:

```powershell
pip install fastapi uvicorn moviepy groq python-dotenv python-multipart
```

### Movie rendering fails

Check that `ffmpeg` is installed and accessible from the command line:

```powershell
ffmpeg -version
```

### Groq authentication fails

Make sure `.env` exists in the project root and includes a valid `GROQ_API_KEY`.

## Security Notes

- Do not commit your `.env` file or API keys.
- Validate and sanitize uploads before exposing this service publicly.
- Consider virus scanning and content restrictions for untrusted files.

## License

Add your preferred license before public distribution.
"# Voxtrim" 
