import tempfile

from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from qwave.models import User, Track, Artist, Album, Genre, Job, track_artists, track_genres
from qwave.config import get_config
from qwave.depends import DBDep, UserDep

router = APIRouter()

# ========================== table item model thingies
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
    added_date:     str

class TrackListResponse(BaseModel):
    tracks:         List[TrackSummary]
    total:          int

class TrackDetail(BaseModel):
    id:             int
    title:          str
    duration:       int
    track_number:   Optional[int]
    artists:        List[ArtistInfo]
    album:          Optional[AlbumInfo]
    genres:         List[GenreInfo]
    lyrics:         Optional[str]
    added_date:     str
    added_by:       UserInfo

# ========================== import flow stuff
class UploadResponse(BaseModel):
    job_id:         int
    track_id:       int
    status:         str

class UpdateTrackRequest(BaseModel):
    title:          Optional[str] = Field(None, min_length = 1, max_length = 255)
    track_number:   Optional[int] = None
    lyrics:         Optional[str] = None

class UpdateTrackResponse(BaseModel):
    id:             int
    updated_fields: List[str]
    track:          dict # maybe make this a model?

class DeleteTrackResponse(BaseModel):
    message:        str
    id:             int

# ========================== some utility thingies
class ArtistListResponse(BaseModel):
    artists:        List[ArtistInfo]

class AddArtistRequest(BaseModel):
    artist_id:      int
    is_primary:     bool = False

class AddArtistResponse(BaseModel):
    message:        str
    track_id:       int
    artist:         ArtistInfo

class GenreRequest(BaseModel):
    genre_id:       int

class MessageResponse(BaseModel):
    message:        str

@router.get("", response_model = TrackListResponse)
def list_tracks(
    user:      UserDep,
    db:        DBDep,
    artist_id: Optional[int] = None,
    album_id:  Optional[int] = None,
    genre_id:  Optional[int] = None,
    added_by:  Optional[int] = None, # user id
    date_from: Optional[str] = None,
    date_to:   Optional[str] = None,
    limit:     int           = 128,
    offset:    int           = 0,
):
    pass

@router.get("/{track_id}", response_model = TrackDetail)
def get_track(user: UserDep, db: DBDep, track_id: int):
    pass

# TODO: allow adding data to track on upload instead of after
@router.post("/upload", response_model = UploadResponse)
async def upload_track(user: UserDep, db: DBDep, file: UploadFile = File(...)):
    pass

@router.patch("/{track_id}", response_model = UpdateTrackResponse)
def update_track(user: UserDep, db: DBDep, track_id: int, request: UpdateTrackRequest): # can i just tack this onto upload_track()?
    pass

# i will hack this club
@router.delete("/{track_id}", response_model = DeleteTrackResponse)
def delete_track(user: UserDep, db: DBDep, track_id: int):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found!")
    # if track.added_by_user_id != user_id:
        # raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't own this track...")

    for path_str in [track.file_path, track.opus_path]:
        if path_str:
            path = Path(path_str)
            if path.exists():
                path.unlink()

    db.delete(track)
    db.commit()
    return DeleteTrackResponse(message = f"Deleted track {track_id}", id = track_id)

@router.get("/{track_id}/artists", response_model = ArtistListResponse)
def get_track_artists(user: UserDep, db: DBDep, track_id: int):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found")
    return ArtistListResponse(
        artists = [ArtistInfo(
            id = a.id, name = a.name, is_primary = is_primary_artist(db, track_id, a.id)
        ) for a in track.artists ]
    )

@router.post("/{track_id}/artists", response_model = AddArtistResponse)
def add_track_artist(user: UserDep, db: DBDep, track_id: int, request: AddArtistRequest):
    pass

@router.delete("/{track_id}/artists/{artist_id}", response_model = MessageResponse)
def remove_track_artist(user: UserDep, db: DBDep, track_id: int, artist_id: int):
    track = db.query(Track).filter(Track.id == track_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found")
    # if track.added_by_user_id != user.id:
        # raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't own this!!")

    db.execute(track_artists.delete().where(
        track_artists.c.track_id == track_id,
        track_artists.c.artist_id == artist_id
    ))
    db.commit()

    return MessageResponse(message = f"Removed artist {artist_id} from track {track_id}")

@router.post("/{track_id}/genres", response_model = MessageResponse)
def add_track_genre(user: UserDep, db: DBDep, track_id: int, request: GenreRequest):
    pass

@router.delete("/{track_id}/genres/{genre_id}", response_model = MessageResponse)
def remove_track_genre(user: UserDep, db: DBDep, track_id: int, genre_id: int):
    track = db.query(Track).filter(Track.id == track_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found!")
    # if track.added_by_user_id != user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't own this...")

    db.execute(
        track_genres.delete().where(
            track_genres.c.track_id == track_id,
            track_genres.c.genre_id == genre_id
    ))
    db.commit()
    return MessageResponse(message = f"Removed genre {genre_id} from {track_id}")

def is_primary_artist(db: Session, track_id: int, artist_id: int) -> bool:
    result = db.execute(
        track_artists.select().where(
            track_artists.c.track_id == track_id,
            track_artists.c.artist_id == artist_id
        )
    ).first()

    return result.is_primary if result else False
