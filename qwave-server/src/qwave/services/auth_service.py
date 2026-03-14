import bcrypt
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session
from qwave.models import User, Session as SessionModel

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def create_user(db: Session, username: str, password: str) -> User:
    if db.query(User).filter(User.username == username).first():
        raise ValueError(f"Username {username} exists")

    user = User(username = username, password_hash = hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_session(db: Session, user_id: int) -> SessionModel:
    token = str(uuid.uuid4())
    expires_at = utc_now() + timedelta(days = 30)

    session = SessionModel(
        user_id = user_id,
        token = token,
        expires_at = expires_at,
        created_at = utc_now()
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return session

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_user_by_token(db: Session, token: str) -> Optional[User]:
    session = db.query(SessionModel).filter(SessionModel.token == token).first()
    if not session:
        return None

    if session.expires_at < utc_now():
        db.delete(session)
        db.commit()
        return None
    
    return session.user

def delete_session(db: Session, token: str) -> bool:
    # returns True on successful delete
    session = db.query(SessionModel).filter(SessionModel.token == token).first()
    if not session:
        return False
    
    db.delete(session)
    db.commit()
    return True