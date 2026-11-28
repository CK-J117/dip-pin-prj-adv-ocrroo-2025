"""Provides a simple API for your basic OCR client

Drive the API to complete "interprocess communication"

Requirements
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi import Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from library_basics import CodingVideo

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")

# We'll create a lightweight "database" for our videos
# You can add uploads later (not required for assessment)
# For now, we will just hardcode are samples


VIDEOS: dict[str, Path] = {
    "demo": Path(BASE_DIR /".."/ "resources" / "oop.mp4")
}
VALID_THEMES = ["", "theme-high-contrast", "theme-yellow-black",
                "theme-blue-white", "theme-cream", "theme-dyslexia",
                "theme-irlen", "theme-photophobia"]

class VideoMetaData(BaseModel):
    fps: float
    frame_count: int
    duration_seconds: float
    _links: dict | None = None


@app.get("/", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, theme: str = "", video_id: str = None):
    if theme not in VALID_THEMES:
        theme = ""
    return templates.TemplateResponse(
        request, "index.html",
        {"theme": theme, "videos": VIDEOS, "video_id": video_id}
    )

@app.get("/video")
def list_videos():
    """List all available videos with HATEOAS-style links."""
    return {
        "count": len(VIDEOS),
        "videos": [
            {
                "id": vid,
                "path": str(path), # Not standard for debug only
                "_links": {
                    "self": f"/video/{vid}",
                    "frame_example": f"/video/{vid}/frame/1.0",
                    "stream": f"/video/{vid}/stream"
                }
            }
            for vid, path in VIDEOS.items()
        ]
    }

def _open_vid_or_404(vid: str) -> CodingVideo:
    path = VIDEOS.get(vid)
    if not path or not path.is_file():
        raise HTTPException(status_code=404, detail=f"Video not found")
    try:
        return CodingVideo(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not open video {e}")

def _meta(video: CodingVideo) -> VideoMetaData:
    return VideoMetaData(
            fps=video.fps,
            frame_count=video.frame_count,
            duration_seconds=video.duration
    )

@app.get("/video/{vid}", response_model=VideoMetaData)
def video(vid: str):
    video = _open_vid_or_404(vid)
    try:
            meta = _meta(video)
            meta._links = {
                "self": f"/video/{vid}",
                "frames": f"/video/{vid}/frame/{{seconds}}",
                "stream": f"/video/{vid}/stream"
            }
            return meta
    finally:
        video.capture.release()


@app.get("/video/{vid}/frame/{t}", response_class=Response)
def video_frame(vid: str, t: float):
    video = _open_vid_or_404(vid)
    try:
        return Response(content=video.get_image_as_bytes(int(t)), media_type="image/png")
    finally:
      video.capture.release()

# TODO: add endpoint to get ocr e.g. /video/{vid}/frame/{t}/ocr
@app.get("/video/{vid}/frame/{t}/ocr")
def video_ocr(vid: str, t: float ):
    video = _open_vid_or_404(vid)
    try:
        text = video.get_text_from_frame(int(t))
        return {"text": text}
    finally:
        video.capture.release()

@app.get("/video/{vid}/stream")
def stream(vid: str):
    path = VIDEOS.get(vid)
    if not path:
        raise HTTPException(404)
    return FileResponse(path, media_type="video/mp4")