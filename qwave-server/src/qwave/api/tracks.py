import tempfile

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from qwave.config import get_config

router = APIRouter()

# =========================== table item model thingies
class ArtistInfo(BaseModel):
    id:             int
    name:           str
    is_primary:     bool

class AlbumInfo(BaseModel):
    id:             int
    title:          str
    release_date:   Optional[str] = None

class GenreInfo(BaseModel):
    id:             int
    name:           str

class UserInfo(BaseModel):
    id:             int
    username:       str

# ========================== track responsesssssssssss
class TrackSummary(BaseModel):
    id:             int
    title:          str
    duration:       int
    artists:        List[ArtistInfo]
    album:          Optional[AlbumInfo]

class abc(BaseModel):
    abc:            int


# ===========
class UpdateTrackResponse(BaseModel):
    id:             int
    updated_fields: List[str]
    track:          dict # maybe make this a model?