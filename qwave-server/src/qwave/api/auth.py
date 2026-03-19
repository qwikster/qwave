from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field

from qwave.models import User
from qwave.depends import DBDep
from qwave.services import auth_service
from qwave.utils.log_item import log_item

router = APIRouter()
# endpoints: /register /login /logout /me

class RegisterRequest(BaseModel):
    username:      str = Field(..., min_length = 3, max_length = 255)
    password:      str = Field(..., min_length = 4)

class LoginRequest(BaseModel):
    username:      str
    password:      str

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    user_id:       int
    username:      str
    created_at:    str

class LoginResponse(BaseModel):
    token:         str
    user_id:       int
    expires_at:    str

class MessageResponse(BaseModel):
    message:       str


def get_current_token(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Missing auth header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Missing auth header or it is in the wrong format")
    return parts[1]

def get_current_user(db: DBDep, token: str = Depends(get_current_token)) -> User:
    user = auth_service.get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token"
        )
    return user


@router.post("/register", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: DBDep):
    try:
        user = auth_service.create_user(db, request.username, request.password)
        log_item(f"New user: {user.username} / {user.id}", "WARN")
        return UserResponse(
            user_id = user.id,
            username = user.username,
            created_at = user.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )

@router.post("/login", response_model = LoginResponse)
def login(request: LoginRequest, db: DBDep):
    user = auth_service.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid username or password"
        )

    session = auth_service.create_session(db, user.id)
    log_item(f"User {user.id} / {user.username} logged in with token {session.token}", "INFO")
    return LoginResponse(
        token = session.token,
        user_id = user.id,
        expires_at = session.expires_at.isoformat()
    )

@router.post("/logout", response_model = MessageResponse)
def logout(db: DBDep, token: str = Depends(get_current_token)):
    success = auth_service.delete_session(db, token)
    if not success:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Session not found")
    return MessageResponse(message = "Logged out successfully")

@router.get("/me", response_model = UserResponse)
def get_current_user_info(user: User = Depends(get_current_user)):
    return UserResponse(user_id = user.id, username = user.username, created_at = user.created_at.isoformat())
