from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func

from qwave.models import Artist, Track, Album, track_artists
from qwave.depends import DBDep, UserDep

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
def list_artists(user: UserDep, db: DBDep, limit: int = 128, offset: int = 0):
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
def get_artist(user: UserDep, db: DBDep, artist_id: int):
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
def get_artist_tracks(user: UserDep, db: DBDep, artist_id: int, limit: int = 128, offset: int = 0,):
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
def get_artist_albums(user: UserDep, db: DBDep, artist_id: int):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Artist not found!"
        )

    # albums where this is the album artist
    as_album_artist = db.query(
        Album, func.count(Track.id).label("track_count")
    ).outerjoin(
        Track, Album.id == Track.album_id
    ).filter(
        Album.album_artist_id == artist_id
    ).group_by(Album.id).all()

    # albums where this artist appears on a track
    as_track_artist = db.query(
        Album, func.count(func.distinct(Track.id)).label("track_count")
    ).join(
        Track, Album.id == Track.album_id
    ).join(
        track_artists, Track.id == track_artists.c.track_id
    ).filter(
        track_artists.c.artist_id == artist_id
    ).group_by(Album.id).all()

    album_ids = set()
    albums = []

    for album, track_count in as_album_artist + as_track_artist:
        if album.id not in album_ids:
            album_ids.add(album.id)
            albums.append(AlbumSummary(
                id = album.id,
                title = album.title,
                release_date = album.release_date.isoformat() if album.release_date else None,
                track_count = track_count or 0
            ))

    return AlbumsResponse(albums = albums)
