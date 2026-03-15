from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from qwave.config import get_config

router = APIRouter()
# /info /config

class ServerInfoResponse(BaseModel):
    name: str
    theme_colors: dict
    logo_url: Optional[str]
    background_url: Optional[str]

class ServerConfigResponse(BaseModel):
    opus_bitrate: int
    acoustid_enabled: bool
    max_upload_size_mb: int

@router.get("/info", response_model = ServerInfoResponse)
def get_server_info():
    config = get_config()
    
    return ServerInfoResponse(
        name = config.server_name,
        theme_colors = {
            "primary": config.theme_primary_color,
            "secondary": config.theme_secondary_color,
        },
        logo_url = config.logo_url,
        background_url = config.background_url
    )

@router.get("/config", response_model = ServerConfigResponse)
def get_server_config():
    config = get_config()

    return ServerConfigResponse(
        opus_bitrate = config.opus_bitrate,
        acoustid_enabled = config.acoustid_enabled,
        max_upload_size_mb = config.max_upload_size_mb
    )