from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from qwave.models import User
from qwave.database import get_db
from qwave.api.auth import get_current_user

DBDep = Annotated[Session, Depends(get_db)]
UserDep = Annotated["User", Depends(get_current_user)]