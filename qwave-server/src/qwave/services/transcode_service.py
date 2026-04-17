from mutagen._file import File as MutagenFile
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
    output_path.parent.mkdir(parents = True, exist_ok = True)

    command = [
        "ffmpeg",
        "-i", str(input_path),      # input
        "-c:a", "libopus",          # use OPUS
        "-b:a", f"{bitrate}k",      # bitrate
        "-vbr", "on",                # variable bitrate (lq source)
        "-compression_level", "10", # TODO: decrease if slow (min file size)
        "-y",                       # overwrite
        str(output_path)            # output
    ]

    try:
        result = subprocess.run(command, capture_output = True, text = True, timeout = 300)

        if result.returncode != 0:
            error = f"ffmpeg failed: {result.stderr}"
            log_item(error, "ERROR")
            return False, error

        if not output_path.exists():
            error = "File not found after transcode"
            log_item(error, "ERROR")
            return False, error

        log_item(f"Transcode complete: {output_path.name}", "SUCCESS")
        return True, None

    except subprocess.TimeoutExpired:
        error = "Transcode timed out!"
        log_item(error, "ERROR")
        return False, error

    except FileNotFoundError:
        error = "ffmpeg is NOT installed >:("
        log_item(error, "ERROR")
        return False, error

    except Exception as e:
        error = f"transcoding failed: {e}"
        log_item(error, "ERROR")
        return False, error

def transcode_verify(
    input_path: Path,
    output_path: Path,
    tolerance: float = 1.0
) -> Tuple[bool, Optional[str]]:
    try:
        input = MutagenFile(input_path)
        output = MutagenFile(output_path)

        if not input or not output:
            return False, "Failed to verify: One or both files are unreadable"

        diff = abs(input.info.length - output.info.length)

        if diff > tolerance:
            return False, f"Failed to verify: {diff:.2f}s difference"

        log_item("Transcode fine", "SUCCESS")
        return True, None

    except Exception as e:
        return False, f"Verification error: {str(e)}"

def get_audio_duration(file_path) -> Optional[float]:
    try:
        audio = mutagen.File(file_path)
        if audio and hasattr(audio, 'info'):
            return audio.info.length
        return None
    except Exception:
        return None
