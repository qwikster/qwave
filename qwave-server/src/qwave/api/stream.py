import os

from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, FileResponse

from qwave.models import Track, User, Job
from qwave.depends import DBDep, UserDep
from qwave.utils.log_item import log_item

router = APIRouter()

@router.get("/{track_id}")
async def stream_track(track_id: int, request: Request, user: UserDep, db: DBDep):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Track not found!!"
        )

    # TODO: better error handling
    file_path = Path(track.opus_path)
    if not file_path.exists():
        if Path(track.file_path).exists():
            job = db.query(Job).filter(Job.track_id == track_id).first()
            if not job:
                detail = f"Track {track_id} is not transcoded and a job does not exist...?"
            else:
                detail = f"Track {track_id} transcode not finished: {job.status}"
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = detail
            )
        else:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Audio file does not exist!!"
            )

    file_size = file_path.stat().st_size
    range_header = request.headers.get("Range")

    if not range_header:
        log_item(f"Streaming {track_id} ({track.title})", "INFO")

        return FileResponse(
            path = file_path,
            media_type = "audio/opus",
            headers = {
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size)
            }
        )

    # try:
