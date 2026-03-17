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

class MetadataExtractor:
    @staticmethod
    def extract(file_path: Path) -> Dict[str, Any]:
        try:
            audio = mutagen.File(file_path)

            if audio is None:
                return MetadataExtractor._empty_metadata(file_path)

            metadata = {
                "duration": audio.info.length if hasattr(audio, 'info') else 0,
                "title": None,
                "artist": None,
                "album": None,
                "album_artist": None,
                "track_number": None,
                "year": None
            }

            match type(audio):
                case "MP3":
                    metadata.update(MetadataExtractor._extract_id3(audio))
                case "FLAC" | "OggVorbis":
                    metadata.update(MetadataExtractor._extract_vorbis(audio))
                case "MP4":
                    metadata.update(MetadataExtractor._extract_mp4(audio))

            if not metadata["title"]:
                metadata["title"] = file_path.stem

            return metadata

        except Exception as e:
            log_item(f"Couldn't extract metadata from {file_path}: {e}", "ERROR")
            return MetadataExtractor._empty_metadata(file_path)

    @staticmethod
    def _empty_metadata(file_path: Path) -> Dict[str, Any]:
        return {
            "duration":     0,
            "title":        file_path.stem or None,
            "artist":       None,
            "album":        None,
            "album_artist": None,
            "track_number": None,
            "year":         None
        }

    @staticmethod
    def _extract_id3(audio) -> Dict[str, Any]:
        tags = {}

    @staticmethod
    def _extract_vorbis(audio) -> Dict[str, Any]:
        tags = {}

    @staticmethod
    def _extract_mp4(audio) -> Dict[str, Any]:
        tags = {}

ver = version("qwave")
BASE_URL = "https://musicbrainz.org/ws/2"
USER_AGENT = f"qWave/{ver} (https://github.com/qwikster/qwave)"

def search_musicbrainz(
    title: Optional[str] = None,
    artist: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    config = get_config()
