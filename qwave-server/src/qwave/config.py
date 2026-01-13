import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    database_url: str
    ...

_config: Optional[Config] = None

def get_config() -> Config:
    if _config is None:
        raise RuntimeError("config is not loaded!!")
    return _config