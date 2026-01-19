from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from qwave.models import Base
from qwave.config import get_config

_engine = None
_SessionLocal = None

def init_db(database_url: str = None):
    global _engine, _SessionLocal
    
    if database_url is None:
        config = get_config()
        database_url = config.database_url
    
    _engine = create_engine(
        database_url, echo = False,
        connect_args = {"check_same_thread": False}
    )
    
    _SessionLocal = sessionmaker(
        autocommit = False,
        autoflush =  False,
        bind =       _engine
    )
    
    return _engine

def create_tables():
    if _engine is None:
        raise RuntimeError("db not initialized!! did you forget to call init_db()?")
    Base.metadata.create_all(bind=_engine)
    
    # Robert')
def drop_tables(): # Students;--
    if _engine is None:
        raise RuntimeError("db not initialized!! did you forget to call init_db()?")
    Base.metadata.drop_all(bind = _engine)
    
def get_session() -> Session:
    if _SessionLocal is None:
        raise RuntimeError("db not initialized!! did you forget to call init_db()?")
    return _SessionLocal()

@contextmanager
def session_scope() -> Generator[Session, None, None]:
    # Get a scope for db operations
    # auto-commit on success, roll back on a failure
    # with session_scope() as session:
    #     user = session.query(User).first
    
    session = get_session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
# for FastAPI
def get_db() -> Generator[Session, None, None]:
    # @router.get("/tracks")
    # def list_tracks(db: Session = Depends(get_db)):
    #     tracks = db.query(Track).all()
    session = get_session()
    try:
        yield session
    finally:
        session.close()