import time
import httpx
import mutagen

from typing import Optional, Dict, Any
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.oggopus import OggOpus
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

        match audio:
            case MP3() | WAVE() | AIFF():
                metadata.update(extract_id3(audio))
            case FLAC() | OggVorbis() | OggOpus():
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

def id3_get(audio, key: str) -> Optional[str]:
    tag = audio.get(key)
    return tag.text[0] if tag and tag.text else None

# vorbis or mp4
def data_get(audio, key: str) -> Optional[str]:
    values = audio.get(key)
    return values[0] if values else None

def extract_id3(audio) -> Dict[str, Any]:
    # what the shit were the ID3 devs on what is this
    tags = {
        "title":        id3_get(audio, "TIT2"),
        "artist":       id3_get(audio, "TPE1"),
        "album":        id3_get(audio, "TALB"),
        "album_artist": id3_get(audio, "TPE2"),
        "genre":        id3_get(audio, "TCON"),
        "track_number": None,
        "year":         None
    }
    try:
        trck = id3_get(audio, "TRCK")
        tags["track_number"] = int(trck.split("/")[0]) if trck else None
    except (ValueError, IndexError):
        pass
    
    try:
        date = id3_get(audio, "TDRC")
        tags["year"] = int(str(date)[:4]) if date else None
    except (ValueError, IndexError):
        pass

    return tags

def extract_vorbis(audio) -> Dict[str, Any]:
    # this is what a Sane Person does
    tags = {
        "title":        data_get(audio, "title"),
        "artist":       data_get(audio, "artist"),
        "album":        data_get(audio, "album"),
        "album_artist": data_get(audio, "albumartist"),
        "genre":        data_get(audio, "genre"),
        "track_number": None,
        "year":         None,
    }

    try:
        track_number = data_get(audio, "tracknumber")
        tags["track_number"] = int(track_number.split("/")[0]) if track_number else None
    except (ValueError, IndexError):
        pass

    try:
        date = data_get(audio, "date")
        tags["year"] = int(date[:4]) if date else None
    except (ValueError, IndexError):
        pass

    return tags

def extract_mp4(audio) -> Dict[str, Any]:
    # NOT AFGAIN NOOOOO
    # \xa9 is © why
    tags = {
        "title":        data_get(audio, "\xa9nam"),
        "artist":       data_get(audio, "\xa9ART"),
        "album":        data_get(audio, "\xa9alb"),
        "album_artist": data_get(audio, "aART"), # why
        "genre":        data_get(audio, "\xa9gen"),
        "track_number": None,
        "year":         None,
    }

    try:
        trkn = audio.get("trkn")
        tags["track_number"] = trkn[0][0] if trkn else None
    except (IndexError, TypeError):
        pass

    try:
        day = data_get(audio, "\xa9day")
        tags["year"] = int(day[:4]) if day else None
    except (IndexError, TypeError):
        pass

    return tags

ver = version("qwave")
BASE_URL = "https://musicbrainz.org/ws/2"
USER_AGENT = f"qWave/{ver} (https://github.com/qwikster/qwave)"

rate_limit = time.time()

def search_musicbrainz(
    title: Optional[str] = None,
    artist: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    global rate_limit
    config = get_config()

    # this is really funny to me for absolutely 0 reason
    if (not config.musicbrainz_enabled) or (not title and not artist):
        return None
    
    query_parts = []
    if title:
        query_parts.append(f'recording:"{title}"')
    if artist:
        query_parts.append(f'recording:"{artist}"')
    query = ' AND '.join(query_parts)

    try:
        if time.time() - rate_limit <= 1:
            time.sleep(1)
            log_item("MusicBrainz rate limit hit!", "WARN")

        with httpx.Client() as client:
            rate_limit = time.time()
            response = client.get(
                f"{BASE_URL}/recording/",
                params = {"query": query, "fmt": "json", "limit": 1},
                headers = {"User-Agent": USER_AGENT},
                timeout = 10.0
            )

            if response.status_code != 200:
                log_item(f"MusicBrainz returned {response.status_code}", "WARN")
                return None
            
            data = response.json()
            if not data.get("recordings"):
                return None
            
            recording = data["recordings"]
            metadata = {
                "title":  recording["title"] if "title" in recording else None,
                "artist": recording["artist-credit"][0]["name"] if "artist_credit" in recording and recording["artist-credit"] else None,
                "album":  recording["releases"][0].get("title") if "releases" in recording and recording["releases"] else None,
            }

            try:
                metadata["year"] = int(recording["releases"][0]["date"][:4]) if "date" in recording["releases"][0] else None
            except (ValueError, IndexError):
                pass

    except Exception as e:
        log_item(f"MusicBrainz search error: {e}", "WARN")