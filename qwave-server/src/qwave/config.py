import os
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    # Server
    server_name: str
    host:        str
    port:        int
    
    # DB
    database_url: str

    # Audio
    opus_bitrate:       int #kbps
    max_upload_size_mb: int

    # Paths
    music_dir: Path
    temp_dir:  Path
    
    # Content ID
    acoustid_enabled:    bool
    acoustid_api_key:    Optional[str]
    musicbrainz_enabled: bool

    # Customizing
    theme_primary_color:   str
    theme_secondary_color: str
    background_url:        Optional[str]
    logo_url:              Optional[str]

_config: Optional[Config] = None

def find_config_file() -> Path:
    # QWAVE_CONFIG env variable, ./config.yaml, ~/.config/qwave/config.yaml, /etc/qwave/config.yaml
    if env_config := os.getenv("QWAVE_CONFIG"):
        path = Path(env_config / "qwave.ini")
        if path.exists():
            return path
        raise FileNotFoundError("couldn't find the config file you set in env!")
    
    locations = [
        Path.cwd() / "qwave.ini",            # Dev (shouldn't happen)
        Path.home() / "qwave" / "qwave.ini", # User install
        Path("/srv/qwave/qwave.ini")         # Server install
    ]
    
    for i in locations:
        if i.exists():
            return i
        
    raise FileNotFoundError("no config file could be found!")

def load_config(config_path: Path = find_config_file()) -> Config:
    global _config

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
        server_name =           data.get("server_name", "qwave"),
        host =                  data.get("host", "0.0.0.0"),
        port =                  data.get("port", 4269),
        database_url =          f"sqlite:///{database_path}",
        opus_bitrate =          data.get("opus_bitrate", 196),
        max_upload_size_mb =    data.get("max_upload_size_mb", 200),
        music_dir =             music_dir,
        temp_dir =              temp_dir,
        acoustid_enabled =      data.get("acoustid_enabled", False),
        acoustid_api_key =      data.get("acoustid_api_key"),
        musicbrainz_enabled =   data.get("musicbrainz_enabled", True),
        theme_primary_color =   data.get("theme_primary_color", "#14f5aa"),
        theme_secondary_color = data.get("theme_secondary_color", "#ff499e"),
        logo_url =              data.get("logo_url"),
        background_url =        data.get("background_url"),
    )
    
    return _config

def get_config() -> Config:
    if _config is None:
        return load_config()
    return _config