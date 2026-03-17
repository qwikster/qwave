import time
import httpx
import mutagen

from typing import Optional, Dict, Any
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from importlib.metadata import version

from qwave.config import get_config
from qwave.utils.logging import log_item

def extract(file_path: Path) -> Dict[str, Any]:
    try:
        audio = mutagen.File(file_path)

        if audio is None:
            return empty_metadata(file_path)

        metadata = {
            "duration": audio.info.length if hasattr(audio, 'info') else 0,
            "title": None,
            "artist": None,
            "album": None,
            "album_artist": None,
            "track_number": None,
            "year": None,
            "genre": None,
        }

        match type(audio):
            case MP3() | WAVE():
                metadata.update(extract_id3(audio))
            case FLAC() | OggVorbis():
                metadata.update(extract_vorbis(audio))
            case MP4():
                metadata.update(extract_mp4(audio))

        if not metadata["title"]:
            metadata["title"] = file_path.stem

        return metadata

    except Exception as e:
        log_item(f"Couldn't extract metadata from {file_path}: {e}", "ERROR")
        return empty_metadata(file_path)

def empty_metadata(file_path: Path) -> Dict[str, Any]:
    return {
        "duration":     0,
        "title":        file_path.stem,
        "artist":       None,
        "album":        None,
        "album_artist": None,
        "track_number": None,
        "year":         None,
        "genre":        None,
    }

def id3_str(audio, tag: str) -> Optional[str]:
    frame = audio.get(tag)
    return frame.text[0] if frame and frame.text else None

def extract_id3(audio) -> Dict[str, Any]:
    tags = {}

    # what the shit were the ID3 devs on what is this
    tags["title"] = str(audio["TIT2"]) or None
    tags["artist"] = str(audio["TPE1"]) or None
    tags["album"] = str(audio["TALB"]) or None
    tags["album_artist"] = str(audio["TPE2"]) or None
    try:
        tags["track_number"] = int(str(audio["TRCK"]).split("/")[0]) or None
        tags["year"] = int(str(audio["TDRC"])[:4]) or None
    except (ValueError, IndexError):
        pass

    return tags

def extract_vorbis(audio) -> Dict[str, Any]:
    tags = {}

    # this is what a Sane Person does
    tags["title"] = audio["title"][0] or None
    tags["artist"] = audio["artist"][0] or None
    tags["album"] = audio["album"][0] or None
    tags["album_artist"] = audio["albumartist"][0] or None
    try:
        tags["track_number"] = int(audio["tracknumber"][0].split("/")[0]) or None
        tags["year"] = int(audio["date"][0][:4]) or None
    except (ValueError, IndexError):
        pass

    return tags

def extract_mp4(audio) -> Dict[str, Any]:
    tags = {}

    # NOT AFGAIN NOOOOO
    tags["title"] = audio["\xa9nam"][0] or None
    tags["artist"] = audio["\xa9ART"][0] or None
    tags["album"] = audio["\xa9alb"][0] or None
    tags["album_artist"] = audio["aART"][0] or None
    try:
        tags["track_number"] = audio["trkn"][0][0] or None
        tags["year"] = int(audio["\xa9day"][0][:4])
    except (ValueError, IndexError, TypeError):
        pass

ver = version("qwave")
BASE_URL = "https://musicbrainz.org/ws/2"
USER_AGENT = f"qWave/{ver} (https://github.com/qwikster/qwave)"

def search_musicbrainz(
    title: Optional[str] = None,
    artist: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    config = get_config()
