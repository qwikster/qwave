from typing import List, Optional
from fastapi import APIRouter, HTTPException, status#, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import func
# from sqlalchemy.orm import Session

from qwave.models import Album, Artist, Track
from qwave.depends import DBDep, UserDep

router = APIRouter()

class AlbumSummary(BaseModel):
    id:           int
    title:        str
    release_date: Optional[str]
    album_artist: Optional[dict]
    track_count:  int

class TrackInAlbum(BaseModel):
    id:           int
    title:        str
    track_number: Optional[int]
    duration:     int
    artists:      List[dict]

class AlbumDetail(BaseModel):
    id:           int
    title:        str
    release_date: Optional[str]
    album_artist: Optional[dict]
    tracks:       List[TrackInAlbum]

class UpdateAlbumRequest(BaseModel):
    title:        Optional[str] = Field(None, min_length = 1, max_length = 255)
    release_date: Optional[str] = None # ISO date string

@router.get("", response_model = dict)
def list_albums(
    user: UserDep, db: DBDep,
    artist_id: Optional[int] = None,
    year: Optional[int] = None,
    limit: int = 128,
    offset: int = 0,
):
    query = db.query(
        Album.id,
        Album.title,
        Album.release_date,
        Album.album_artist_id,
        Artist.name.label('artist_name'),
        func.count(Track.id).label('track_count')
    ).outerjoin(
        Artist, Album.album_artist_id == Artist.id
    ).outerjoin(
        Track, Album.id == Track.album_id
    ).group_by(Album.id)

    if artist_id:
        query = query.filter(Album.album_artist_id == artist_id)

    if year:
        query = query.filter(func.strftime('%Y', Album.release_date) == str(year))

    query = query.order_by(Album.title)
    total = query.count()
    albums = query.limit(limit).offset(offset).all()

    return {
        "albums": [
            {
                "id": a.id,
                "title": a.title,
                "release_date": a.release_date.isoformat() if a.release_date else None,
                "album_artist": {
                    "id": a.album_artist_id,
                    "name": a.artist_name
                } if a.album_artist_id else None,
                "track_count": a.track_count or 0
            }
            for a in albums
        ], "total": total
    }

@router.get("/{album_id}", response_model = dict)
def get_album(user: UserDep, db: DBDep, album_id: int):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Album not found!"
        )

    tracks = db.query(Track).filter(
        Track.album_id == album_id
    ).order_by(
        Track.track_number.nullslast(),
        Track.title
    ).all()

    return {
        "id": album.id,
        "title": album.title,
        "release_date": album.release_date.isoformat() if album.release_date else None,
        "album_artist": {
            "id": album.album_artist.id,
            "name": album.album_artist.name
        } if album.album_artist else None,
        "tracks" : [
            {
                "id": t.id,
                "title": t.title,
                "track_number": t.track_number,
                "duration": int(t.duration),
                "artists": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "is_primary": db.query(db.query(Track).join(Track.artists).filter(
                            Track.id == t.id, Artist.id == a.id
                        ).exists()).scalar()
                    }
                    for a in t.artists
                ]
            }
            for t in tracks
        ]
    }

@router.patch("/{album_id}", response_model = dict)
def update_album(user: UserDep, db: DBDep, album_id: int, request: UpdateAlbumRequest):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Album not found!"
        )

    # owns_track = db.query(Track).filter(
    #     Track.album_id == album_id,
    #     Track.added_by_user_id == user.id
    # ).first()
    # if not owns_track:
    #     raise HTTPException(
    #         status_code = status.HTTP_403_FORBIDDEN,
    #         detail = "You do not own this album"
    #     )

    updated_fields = []

    if request.title is not None:
        album.title = request.title
        updated_fields.append("title")

    if request.release_date is not None:
        try:
            album.release_date = datetime.fromisoformat(request.release_date)
            updated_fields.append("release_date")
        except ValueError:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Invalid date format!"
            )

    if not request.title and not request.release_date:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Nothing to modify!"
        )

    db.commit()
    db.refresh(album)

    return {
        "id": album.id,
        "updated_fields": updated_fields,
        "album": {
            "id": album.id,
            "title": album.title,
            "release_date": album.release_date.isoformat() if album.release_date else None,
            "album_artist": {
                "id": album.album_artist.id,
                "name": album.album_artist.name
            } if album.album_artist else None
        }
    }
