from typing import List, Optional, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from qwave.models import Track, Album, Artist
from qwave.depends import DBDep, UserDep

router = APIRouter()

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

    # pattern = f"%{query}%"

    if type in ["tracks", "all"]:
        tracks = db.query(Track).filter(...).limit(limit).all()
        results["tracks"] = [... for track in tracks]

    if type in ["albums", "all"]:
        albums = db.query(Album).filter(...).limit(limit).all()
        results["albums"] = [... for album in albums]

    if type in ["artists", "all"]:
        artists = db.query(Artist).filter(...).limit(limit).all()
        results["artists"] = [... for artist in artists]

    return SearchResponse(**results)
