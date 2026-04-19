# save for full release
from typing import Optional
from fastapi import APIRouter
from qwave.depends import DBDep, UserDep

router = APIRouter()

@router.get("", response_model = ...)
def get_playlists(db: DBDep, user: UserDep, user_id: Optional[int]):
    ...

@router.get("/{id}", response_model = ...)
def get_playlist(db: DBDep, user: UserDep, id: int):
    ...

@router.post("", response_model = ...)
def create_playlist(
    db: DBDep,
    user: UserDep,
    name: str,
    is_public: Optional[int],
    tracks: Optional[list]
):
    ...

@router.patch("/{id}", response_model = ...)
def rename_playlist(
    db: DBDep,
    user: UserDep,
    id: int,
    name: Optional[int],
    is_public: Optional[bool]
):
    ...

@router.delete("/{id}", response_model = ...)
def delete_playlist(db: DBDep, user: UserDep, id: int):
    ...

@router.post("/{id}/tracks", response_model = ...)
def add_tracks(db: DBDep, user: UserDep, id: int, tracks: list):
    ...

@router.delete("/{id}/tracks", response_model = ...)
def remove_tracks(db: DBDep, user: UserDep, id: int, tracks: list):
    ...

@router.patch("/{id}/tracks", response_model = ...)
def reorder_playlist(db: DBDep, user: UserDep, id: int, track_order: list):
    ...
