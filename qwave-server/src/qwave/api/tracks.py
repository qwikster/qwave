import tempfile

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from qwave.config import get_config

router = APIRouter()

class ArtistInfo(BaseModel):
    id: int
    name: