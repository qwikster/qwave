import mutagen
import subprocess

from typing import Optional, Tuple
from pathlib import Path

from qwave.config import get_config
from qwave.utils.log_item import log_item

def transcode(
    input_path: Path,
    output_path: Path,
    bitrate: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    # (success, error_message)
    config = get_config()
    bitrate = config.opus_bitrate if bitrate is None else bitrate

    return True, None

def transcode_verify(
    input_path: Path,
    output_path: Path,
    tolerance: float = 1.0
) -> Tuple[bool, Optional[str]]:
    original = mutagen.File(input_path)
    output = mutagen.File(output_path)

    if not original or not output:
        return False, "One or both files are unreadable"

    return True, None

def get_audio_duration(file_path) -> Optional[float]:
    try:
        audio = mutagen.File(file_path)
        if audio and hasattr(audio, 'info'):
            return audio.info.length
        return None
    except Exception:
        return None
