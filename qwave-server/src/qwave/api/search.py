from typing import List, Literal
from fastapi import APIRouter
from pydantic import BaseModel

from qwave.models import Track, Album, Artist
from qwave.depends import DBDep, UserDep

router = APIRouter()

class TrackResult(BaseModel):
    id:      int
    title:   str
    artists: List[dict]

class AlbumResult(BaseModel):
    id:      int
    title:   str

class ArtistResult(BaseModel):
    id:      int
    name:    str

class SearchResponse(BaseModel):
    tracks:  List[TrackResult]
    albums:  List[AlbumResult]
    artists: List[ArtistResult]

@router.get("", response_model = SearchResponse)
def search(
    user:  UserDep,
    db:    DBDep,
    query: str,
    type:  Literal["all", "tracks", "albums", "artists"] = "all",
    limit: int = 20
):
    results = {
        "tracks":  [],
        "albums":  [],
        "artists": []
    }

    pattern = f"%{query}%"

    if type in ["tracks", "all"]:
        tracks = db.query(Track).filter(Track.title.ilike(pattern)).limit(limit).all()
        results["tracks"] = [TrackResult(
            id = track.id,
            title = track.title,
            artists = [{"id": a.id, "name": a.name} for a in track.artists]
        ) for track in tracks]

    if type in ["albums", "all"]:
        albums = db.query(Album).filter(Album.title.ilike(pattern)).limit(limit).all()
        results["albums"] = [AlbumResult(id = album.id, title = album.title) for album in albums]

    if type in ["artists", "all"]:
        artists = db.query(Artist).filter(Artist.name.ilike(pattern)).filter(Artist.tracks.any()).limit(limit).all()
        results["artists"] = [ArtistResult(id = artist.id, name = artist.name) for artist in artists]

    return SearchResponse(**results)
