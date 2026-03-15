from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from qwave.models import Artist, Track, Album, track_artists
from qwave.database import get_db
from qwave.api.auth import get_current_user

router = APIRouter()

class ArtistSummary(BaseModel):
    id: int
    name: str
    track_count: int
    album_count: int

    class Config:
        from_attributes = True

class ArtistDetail(BaseModel):
    id: int
    name: str
    track_count: int
    album_count: int

    class Config:
        from_attributes = True

class ArtistListResponse(BaseModel):
    artists: List[ArtistSummary]
    total: int

class TrackSummary(BaseModel):
    id: int
    title: str
    duration: float
    album: Optional[dict]

    class Config:
        from_attributes = True

class TracksResponse(BaseModel):
    tracks: List[TrackSummary]
    total: int

class AlbumSummary(BaseModel):
    id: int
    title: str
    release_date: Optional[str]
    track_count: int

    class Config:
        from_attributes = True

class AlbumsResponse(BaseModel):
    albums: List[AlbumSummary]

@router.get("", response_model = ArtistListResponse)
def list_artists(
    limit: int = 100,
    offset: int = 0,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    artists_query = db.query(
        Artist,
        func.count(func.distinct(track_artists.c.track_id)).label('track_count'),
        func.count(func.distinct(Album.id)).label('album_count')
    ).outerjoin(
        track_artists, Artist.id == track_artists.c.artist_id
    ).outerjoin(
        Album, Artist.id == Album.album_artist_id
    ).group_by(Artist.id)

    total = artists_query.count()
    artists_data = artists_query.offset(offset).limit(limit).all()

    artists = [
        ArtistSummary(
            id = artist.id,
            name = artist.name,
            track_count = track_count or 0,
            album_count = album_count or 0
        )
        for artist, track_count, album_count in artists_data
    ]

    return ArtistListResponse(artists = artists, total = total)