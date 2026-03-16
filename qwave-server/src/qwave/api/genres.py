from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from qwave.models import Genre, Track, track_genres
from qwave.api.auth import get_current_user
from qwave.database import get_db

router = APIRouter()

class CreateGenreRequest(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 128)

class GenreSummary(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class GenreResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class GenresResponse(BaseModel):
    genres: List[GenreSummary]

class TrackSummary(BaseModel):
    id: int
    title: str
    duration: float
    artists: List[dict]

    class Config:
        from_attributes = True

class TracksResponse(BaseModel):
    tracks: List[TrackSummary]
    total: int


@router.get("", response_model = GenresResponse)
def list_genres(
    user = Depends[get_current_user],
    db: Session = Depends[get_current_user]
):
    genres_query = db.query(
        Genre, func.count(track_genres.c.track_id).label('track_count')
    ).outerjoin(
        track_genres, Genre.id == track_genres.c.genre_id
    ).group_by(Genre.id)

    genres_data = genres_query.all()

    genres = [
        GenreSummary(
            id = genre.id,
            name = genre.name,
            track_count = track_count or 0
        )
        for genre, track_count in genres_data
    ]
    
    return GenresResponse(genres=genres)

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

@