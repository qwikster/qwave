import re
import magic
from typing import Optional, Tuple
from pathlib import Path

from qwave.config import get_config

ALLOWED_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".opus", ".m4a"}
ALLOWED_MIME_TYPES = {
    "audio/mpeg",
    "audio/flac",
    "audio/x-flac",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/opus",
    "audio/x-m4a",
    "audio/mp4",
}

# returns (is_valid, error_message)
def validate_audio_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, f"File type {file_path.suffix} not allowed."

    try:
        mime = magic.from_file(str(file_path), mime = True)
        if mime not in ALLOWED_MIME_TYPES:
            return False, f"File is {mime}, not an audio file."

    except Exception as e:
        return False, f"Could not detect file type: {e}"

    return True, None

def sanitize(name: str) -> str:
    name = name.replace("/", "-" ).replace("\\", "-")
    name = name.replace(":", " -").replace("|", "-")
    name = name.replace('"', "'" ).replace("*", "")
    name = name.replace("<", "(" ).replace(">", ")")
    name = name.replace("?", "").strip(". ")
    name = re.sub(r'\s+', ' ', name) # remove double spaces
    return name or "Unknown"

def build_track_path(
    artist_name: str,
    track_title: str,
    album_title: Optional[str] = None,
    album_year:  Optional[int] = None,
    track_number: Optional[int] = None
) -> Path:
    config = get_config()
    base_dir = config.music_dir

    s_artist = sanitize(artist_name)
    s_track  = sanitize(track_title)

    if album_title:
        s_album = sanitize(album_title)
        if album_year:
            album_dir = f"{s_album} ({album_year})"
        else:
            album_dir = s_album

        if track_number:
            filename = f"{track_number:02d} - {s_track}.opus"
        else:
            filename = f"{s_track}.opus"

        path = base_dir / s_artist / album_dir / filename
    else:
        filename = f"{s_track}.opus"
        path = base_dir / s_artist / "singles" / filename

    if path.exists():
        counter = 2
        while path.exists():
            if album_title and track_number:
                filename = f"{track_number:02d} - {s_track} ({counter}).opus"
            else:
                filename = f"{s_track} ({counter}).opus"
            path = path.parent / filename
            counter += 1

    path.parent.mkdir(parents = True, exist_ok = True)

    return path
