from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Status
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from qwave.models import Album, Artist, Track
from qwave.database import get_db
from qwave.api.auth import get_current_user

router = APIRouter()

class AlbumSummary(BaseModel):

class TrackInAlbum(BaseModel):

class AlbumDetail(BaseModel):

class UpdateAlbumRequest(BaseModel):


@router.get("", response_model = dict)
def list_albums(

):
    query = db.query()

@router.get("/{album_id}", response_model = dict)
def get_album(

):
    album = db.query(Album)

@router.patch("/{album_id}", response_model = dict)
def update_album(

):
    album = db.query()

