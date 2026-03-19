from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from qwave.models import Genre, Track, track_genres
from qwave.api.auth import get_current_user
from qwave.database import get_db

router = APIRouter()

class CreateGenreRequest(BaseModel):
    name:          str = Field(..., min_length = 1, max_length = 128)

class GenreSummary(BaseModel):
    id:            int
    name:          str
    track_count:   int

class GenreResponse(BaseModel):
    model_config = {"from_attributes": True}
    id:            int
    name:          str
    
@router.get("", response_model = dict)
def list_genres(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    genres = db.query(
        Genre.id,
        Genre.name,
        func.count(Track.id).label('track_count')
    ).outerjoin(
        track_genres, Genre.id == track_genres.c.genre_id
    ).outerjoin(
        Track, track_genres.c.track_id == Track.id
    ).group_by(Genre.id).order_by(Genre.name).all()

    return {
        "genres": [
            {
                "id": g.id,
                "name": g.name,
                "track_count": g.track_count or 0
            }
            for g in genres
        ]
    }

@router.post("", response_model = GenreResponse, status_code = status.HTTP_201_CREATED)
def create_genre(
    request: CreateGenreRequest,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Genre).filter(
        func.lower(Genre.name) == request.name.lower()
    ).first()
    
    if existing:
        return GenreResponse(id = existing.id, name = existing.name)
    
    genre = Genre(name = request.name)
    db.add(genre)
    db.commit()
    db.refresh(genre)

    return GenreResponse(id = genre.id, name = genre.name)

@router.get("/{genre_id}/tracks", response_model = dict)
def get_genre_tracks(
    genre_id: int,
    limit: int = 128,
    offset: int = 0,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Genre not found!"
        )

    tracks_query = db.query(Track).join(
        track_genres
    ).filter(track_genres.c.genre_id == genre_id).order_by(Track.title)

    total = tracks_query.count()
    tracks = tracks_query.offset(offset).limit(limit).all()

    return {
        "tracks": [
            {
                "id": t.id,
                "title": t.title,
                "duration": int(t.duration),
                "artists": [] # TODO: populate when i finish artists.py
            }                 # ...im gonna forget about this
            for t in tracks
        ],
        "total": total
    }