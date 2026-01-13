import os
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    database_url: str
    ... # TODO: add all the thingies

_config: Optional[Config] = None

def find_config_file() -> Path:
    # QWAVE_CONFIG env variable, ./config.yaml, ~/.config/qwave/config.yaml, /etc/qwave/config.yaml
    return Path.home() # TODO: search through standard locations

def load_config(config_path: Optional[Path] = None) -> Config:
    global _config
    
    if config_path is None:
        config_path = find_config_file()

    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    def resolve_path(path_str: str) -> Path:
        path = Path(path_str)
        if not path.is_absolute():
            # make relative paths to config file location, should only be true in development or odd clone installs
            path = (config_path.parent / path).resolve()
        return path
    
    database_path = resolve_path(data["database_path"])
    music_dir =     resolve_path(data["music_dir"])
    temp_dir =      resolve_path(data["temp_dir"])
    
    # TODO: make sure they're created in the init.py run as well as pick locations
    _config = Config(
        ... = ...,
        ... = ..., 
    )
    
    return _config

def get_config() -> Config:
    if _config is None:
        raise RuntimeError("config is not loaded!!")
    return _config