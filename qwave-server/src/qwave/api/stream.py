from typing import Generator
from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import StreamingResponse, FileResponse

from qwave.models import Track, Job
from qwave.depends import DBDep, UserDep
from qwave.utils.log_item import log_item

router = APIRouter()

def stream_range(
    file_path: Path,
    start: int, end: int,
    chunk_size: int = 8192
) -> Generator[bytes, None, None]:
    with open(file_path, "rb") as f:
        f.seek(start)
        remaining = end - start + 1

        while remaining:
            chunk_size = min(chunk_size, remaining)
            data = f.read(chunk_size)
            if not data:
                break
            remaining -= len(data)
            yield data

@router.get("/{track_id}")
# HACK: remove UserDep for html testing, or curl | mpv -
async def stream_track(track_id: int, request: Request, db: DBDep, user: UserDep):
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

    try:
        range_str = range_header.replace("bytes=", "").strip()
        range_parts = range_str.split("-")

        start = int(range_parts[0]) if range_parts[0] else 0
        end = int(range_parts[1]) if len(range_parts) > 1 and range_parts[1] else file_size - 1

        if start >= file_size or end >= file_size or start > end:
            raise HTTPException(
                status_code = status.HTTP_416_RANGE_NOT_SATISFIABLE,
                headers = {"Content-Range": f"bytes */{file_size}"}
            )

        content_length = end - start + 1
        log_item(f"Streaming {track_id} ({track.title}) at range {start}-{end}/{file_size}", "INFO")

        return StreamingResponse(
            stream_range(file_path, start, end),
            status_code = 206,
            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length)
            }
        )

    except ValueError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid Range header."
        )
