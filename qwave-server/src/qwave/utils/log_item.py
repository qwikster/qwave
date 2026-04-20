from typing import Optional
from pathlib import Path
from datetime import datetime
from qwave.config import find_config_file

symbols = {
    "ERROR": "X",
    "INFO": "*",
    "WARN": "!",
    "SUCCESS": "✓",
    "JOB": ">",
}

def clear_log(file: Path = find_config_file().parent / 'qwave.log'):
    if not file.exists():
        return 0
    file.rename('qwave_old.log')
    with open(file, 'w') as f:
        f.write(f"[{datetime.now().strftime('%x %X')}] Log cleared\n")
        f.write("===============================\n")

def get_log_path(config_path: Path = find_config_file()) -> Path:
    return config_path.parent

def log_item(content: str, type: str, timestamp: Optional[str] = None, log_path: Path = get_log_path()):
    if timestamp is None:
        timestamp = datetime.now().strftime("%x %X")

    sym = symbols.get(type.upper(), "what did you do")
    message = f"[{timestamp}] [{sym}] {type.upper()}: {content}\n"
    print(message, end = "")
    with open(log_path / 'qwave.log', 'a') as f:
        f.write(message)
