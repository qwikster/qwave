
import shutil

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from qwave.config import get_config
from qwave.models import Track, Artist, Album, Job, Genre, track_artists, track_genres
from qwave.utils.log_item import log_item
from qwave.services.file_service import sanitize, validate_audio_file
from qwave.services.metadata_service import extract, search_musicbrainz

def handle_upload(
    db: Session,
    file_path: Path,
    filename: str,
    user_id: int
) -> Dict[str, Any]:
    config = get_config()

    is_valid, error = validate_audio_file(file_path)
    if not is_valid:
        raise ValueError(error)

    temp_file = config.temp_dir / f"{sanitize(filename)}"
    shutil.copy(file_path, temp_file)

    log_item(f"Processing metadata for {sanitize(filename)}", "INFO")
    metadata = extract(temp_file)

    needs_analysis = not metadata.get('title') or not metadata.get('artist')

    if needs_analysis and config.musicbrainz_enabled:
        mb_metadata = search_musicbrainz(title = metadata.get("title"), artist = metadata.get("artist"))
        if mb_metadata:
            for key, value in mb_metadata.items():
                if value and not metadata.get(key):
                    metadata[key] = value

    needs_review = not metadata.get("title") or not metadata.get("artist")
    artist_name = metadata.get("artist", "")
    if not artist_name:
        artist_name = "Unknown Artist"
    artist = find_artist(db, artist_name)
    album = None

    if metadata.get("album"):
        album = find_album(
            db,
            title = metadata["album"],
            artist_id = artist.id,
            year = metadata.get("year")
        )

    track = Track(
        title =            metadata.get("title", filename),
        duration =         metadata.get("duration", 0),
        file_path =        str(temp_file),
        opus_path =        None,
        track_number =     metadata.get("track_number"),
        album_id =         album.id if album else None,
        added_by_user_id = user_id,
        needs_review =     needs_review,
    )
    db.add(track)
    db.flush()
    db.execute(track_artists.insert().values(
        track_id =   track.id,
        artist_id =  artist.id,
        is_primary = True
    ))

    if metadata.get("genre"):
        genre = find_genre(db, metadata["genre"])
        db.execute(track_genres.insert().values(
            track_id = track.id,
            genre_id = genre.id
        ))

    job = Job(
        type =    "transcode",
        status =  "pending",
        track_id = track.id
    )
    db.add(job)
    db.commit()
    db.refresh(track)
    db.refresh(job)

    log_item(f"Track {track.id} created, job {job.id} queued", "SUCCESS")

    return {
        "track_id":     track.id,
        "job_id":       job.id,
        "needs_review": needs_review,
        "status":       "needs_review" if needs_review else "pending"
    }


def find_artist(db: Session, name: str) -> Artist:
    artist = db.query(Artist).filter(Artist.name == name).first()
    if not artist:
        artist = Artist(name = name)
        db.add(artist)
        db.flush()
    return artist

def find_album(
    db: Session,
    title: str,
    artist_id: int,
    year: Optional[int] = None
) -> Album:
    query = db.query(Album).filter(
        Album.title == title,
        Album.album_artist_id == artist_id
    )

    if year:
        release_date = datetime(year, 1, 1)
        query = query.filter(Album.release_date == release_date)

    album = query.first()
    if not album:
        album = Album(
            title = title,
            album_artist_id = artist_id,
            release_date = datetime(year, 1, 1) if year else None
        )
        db.add(album)
        db.flush()
    return album


def find_genre(db: Session, name: str) -> Genre:
    genre = db.query(Genre).filter(
        func.lower(Genre.name) == name.lower()
    ).first()

    if not genre:
        genre = Genre(name = name)
        db.add(genre)
        db.flush()
    return genre
