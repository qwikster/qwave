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
    model_config = {"from_attributes": True}
    id:            int
    name:          str
    track_count:   int
    album_count:   int

class ArtistDetail(BaseModel):
    model_config = {"from_attributes": True}
    id:            int
    name:          str
    track_count:   int
    album_count:   int

class ArtistListResponse(BaseModel):
    artists:       List[ArtistSummary]
    total:         int

class TrackSummary(BaseModel):
    model_config = {"from_attributes": True}
    id:            int
    title:         str
    duration:      float
    album:         Optional[dict]

class TracksResponse(BaseModel):
    tracks:        List[TrackSummary]
    total:         int

class AlbumSummary(BaseModel):
    model_config = {"from_attributes": True}
    id:            int
    title:         str
    release_date:  Optional[str]
    track_count:   int

class AlbumsResponse(BaseModel):
    albums:        List[AlbumSummary]

@router.get("", response_model = ArtistListResponse)
def list_artists(
    limit: int = 128,
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

@router.get("/{artist_id}", response_model = ArtistDetail)
def get_artist(
    artist_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Artist not found"
        )

    track_count = db.query(func.count(track_artists.c.track_id)).filter(
        track_artists.c.artist_id == artist_id
    ).scalar() or 0

    album_count = db.query(func.count(Album.id)).filter(
        Album.album_artist_id == artist_id
    ).scalar() or 0

    return ArtistDetail(
        id = artist.id,
        name = artist.name,
        track_count = track_count,
        album_count = album_count
    )

@router.get("/{artist_id}/tracks", response_model = TracksResponse)
def get_artist_tracks(
    artist_id: int,
    limit: int = 128,
    offset: int = 0,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Artist not found"
        )
    
    tracks_query = db.query(Track).join(
        track_artists, Track.id == track_artists.c.track_id
    ).filter(track_artists.c.artist_id == artist_id)

    total = tracks_query.count()
    tracks = tracks_query.offset(offset).limit(limit).all()

    track_summaries = [
        TrackSummary(
            id = track.id,
            title = track.title,
            duration = track.duration,
            album = {
                "id": track.album.id,
                "title": track.album.title
            } if track.album else None
        )
        for track in tracks
    ]

    return TracksResponse(tracks = track_summaries, total = total)

@router.get("/{artist_id}/albums", response_model = AlbumsResponse)
def get_artist_albums(
    artist_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Artist not found!"
        )
    
    albums_as_artist = db.query(Album).filter(
        Album.album_artist_id == artist_id
    ).all()

    albums_with_tracks = db.query(Album).join(
        Track, Album.id == Track.album_id
    ).join(
        track_artists, Track.id == track_artists.c.track_id
    ).filter(track_artists.c.artist_id == artist_id).distinct().all()

    album_ids = set()
    albums = []

    for album in albums_as_artist + albums_with_tracks:
        if album.id not in album_ids:
            album_ids.add(album.id)
            track_count = db.query(func.count(Track.id)).filter(
                Track.album_id == album.id
            ).scalar() or 0

            albums.append(AlbumSummary(
                id = album.id,
                title = album.title,
                release_date = album.release_date.isoformat() if album.release_date else None,
                track_count = track_count
            ))
    return AlbumsResponse(albums = albums)