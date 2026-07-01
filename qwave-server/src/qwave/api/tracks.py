import tempfile

from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Session, selectinload, joinedload
from starlette.status import HTTP_403_FORBIDDEN

from qwave.models import Track, Artist, Genre, Job, track_artists, track_genres
from qwave.config import get_config
from qwave.depends import DBDep, UserDep
from qwave.services import import_service
# from qwave.utils.log_item import log_item
from qwave.workers.worker import queue_job

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
    query = db.query(Track)

    if artist_id:
        query = query.join(track_artists).filter(track_artists.c.artist_id == artist_id)
    if album_id:
        query = query.filter(Track.album_id == album_id)
    if genre_id:
        query = query.join(track_genres).filter(track_genres.c.genre_id == genre_id)
    if added_by:
        query = query.filter(Track.added_by_user_id == added_by)
    if date_from:
        query = query.filter(Track.added_date >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.filter(Track.added_date <= datetime.fromisoformat(date_to))

    total = query.count()
    tracks = query.limit(limit).offset(offset).all()

    primary_map = load_primary_map(db, [t.id for t in  tracks])

    return TrackListResponse(
        tracks = [
            TrackSummary(
                id = t.id,
                title = t.title,
                duration = int(t.duration),
                artists = [
                    ArtistInfo(
                        id = a.id,
                        name = a.name,
                        is_primary = primary_map.get((t.id, a.id), False)
                    ) for a in t.artists
                ],
                album = AlbumInfo(
                    id = t.album.id,
                    title = t.album.title,
                    release_date = t.album.release_date.isoformat() if t.album.release_date else None
                ) if t.album else None,
                added_date = t.added_date.isoformat()
            ) for t in tracks
        ], total = total
    )


@router.get("/{track_id}", response_model = TrackDetail)
def get_track(user: UserDep, db: DBDep, track_id: int):
    track = db.query(Track).options(
        selectinload(Track.artists),
        joinedload(Track.album),
        selectinload(Track.genres),
        joinedload(Track.added_by)
    ).filter(Track.id == track_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found!")

    primary_map = load_primary_map(db, [track_id])

    return TrackDetail(
        id = track.id,
        title = track.title,
        duration = int(track.duration),
        track_number = track.track_number,
        artists = [
            ArtistInfo(
                id = a.id, name = a.name,
                is_primary = primary_map.get((track.id, a.id), False)
            ) for a in track.artists
        ],
        album = AlbumInfo(
            id = track.album.id,
            title = track.album.title,
            release_date = track.album.release_date.isoformat() if track.album.release_date else None
        ) if track.album else None,
        genres = [GenreInfo(id = g.id, name = g.name) for g in track.genres],
        lyrics = track.lyrics,
        added_date = track.added_date.isoformat(),
        added_by = UserInfo(id = track.added_by.id, username = track.added_by.username)
    )

# TODO: MAYBE: allow adding data to track on upload instead of after
@router.post("/upload", response_model = UploadResponse)
async def upload_track(user: UserDep, db: DBDep, file: UploadFile = File(...)):
    # raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail = "uploads are disabled!")

    config = get_config()
    max_size = config.max_upload_size_mb * (1024 ** 2)

    if not file.filename:
        raise Exception("WHAT DID YOU DO") # just here to get pyright to shut up

    with tempfile.NamedTemporaryFile(delete = False, suffix = Path(file.filename).suffix) as tmp:
        content = await file.read()
        if len(content) > max_size:
            Path(tmp.name).unlink()
            raise HTTPException(status_code = status.HTTP_413_CONTENT_TOO_LARGE, detail = "file too large!")
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        result = import_service.handle_upload(db = db, file_path = tmp_path, filename = file.filename, user_id = user.id)
        job = db.query(Job).filter(Job.id == result["job_id"]).first()
        if job:
            queue_job(job)

        return UploadResponse(
            job_id = result["job_id"],
            track_id = result["track_id"],
            status = result["status"]
        )

    except ValueError as e:
        tmp_path.unlink()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = str(e))

    finally:
        if tmp_path.exists():
            tmp_path.unlink()

# TODO: add the rest of the fields? gotta do it different
@router.patch("/{track_id}", response_model = UpdateTrackResponse)
def update_track(user: UserDep, db: DBDep, track_id: int, request: UpdateTrackRequest): # can i just tack this onto upload_track()?
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "Trakc not found!")
    # too lazy to add the legacy permission check

    updated_fields = []

    if request.title is not None:
        track.title = request.title
        updated_fields.append("title")
    if request.track_number is not None:
        track.track_number = request.track_number
        updated_fields.append("track_number")
    if request.lyrics is not None:
        track.lyrics = request.lyrics
        updated_fields.append("lyrics")

    db.commit()
    db.refresh(track)

    return UpdateTrackResponse(
        id = track.id,
        updated_fields = updated_fields,
        track = {
            "id": track.id,
            "title": track.title,
            "track_number": track.track_number,
            "lyrics": track.lyrics
        }
    )

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
    track = db.query(Track).options(selectinload(Track.artists)).filter(Track.id == track_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found")

    primary_map = load_primary_map(db, [track_id])

    return ArtistListResponse(
        artists = [ArtistInfo(
            id = a.id, name = a.name,
            is_primary = primary_map.get((track_id, a.id), False)
        ) for a in track.artists ]
    )


@router.post("/{track_id}/artists", response_model = AddArtistResponse)
def add_track_artist(user: UserDep, db: DBDep, track_id: int, request: AddArtistRequest):
    track = db.query(Track).filter(Track.id == track_id).first()
    artist = db.query(Artist).filter(Artist.id == request.artist_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found...")
    if not artist:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Artist not found...")
    # if track.added_by_user_id != user.id:
        # raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't own this...")

    existing = db.execute( track_artists.select().where(
        track_artists.c.track_id == track_id,
        track_artists.c.artist_id == request.artist_id
    )).first()

    if existing:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Artist already selected!")

    db.execute(
    track_artists.insert().values(
        track_id = track_id,
        artist_id = request.artist_id,
        is_primary = request.is_primary
    ))
    db.commit()

    return AddArtistResponse(
        message = "Artist added :)",
        track_id = track_id,
        artist = ArtistInfo(id = artist.id, name = artist.name, is_primary = request.is_primary)
    )


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
    track = db.query(Track).filter(Track.id == track_id).first()
    genre = db.query(Genre).filter(Genre.id == request.genre_id).first()

    if not track:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Track not found!")
    if not genre:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Genre not found!")
    # auth here?

    db.execute(
        track_genres.insert().values(
            track_id = track_id,
            genre_id = request.genre_id
        )
    )
    db.commit()
    return MessageResponse(message = "Genre added!")

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

# semideprecated (??)
def is_primary_artist(db: Session, track_id: int, artist_id: int) -> bool:
    result = db.execute(
        track_artists.select().where(
            track_artists.c.track_id == track_id,
            track_artists.c.artist_id == artist_id
        )
    ).first()

    return result.is_primary if result else False

def load_primary_map(db: Session, track_ids: list[int]) -> dict[tuple[int, int], bool]:
    if not track_ids:
        return {}
    rows = db.execute(
        track_artists.select().where(
            track_artists.c.track_id.in_(track_ids)
        )
    ).fetchall()
    return {(r.track_id, r.artist_id): r.is_primary for r in rows}
