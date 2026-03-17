from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Text, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

def utc_now():
    return datetime.now(timezone.utc)

class Base(DeclarativeBase):
    pass

# ASSOCIATION TABLES
track_artists = Table(
    "track_artists",
    Base.metadata,
    Column("track_id",   Integer, ForeignKey("tracks.id",  ondelete = "CASCADE"), primary_key = True),
    Column("artist_id",  Integer, ForeignKey("artists.id", ondelete = "CASCADE"), primary_key = True),
    Column("is_primary", Boolean, default = False, nullable = False)
)

track_genres = Table(
    "track_genres",
    Base.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id", ondelete = "CASCADE"), primary_key = True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete = "CASCADE"), primary_key = True)
)

playlist_tracks = Table(
    "playlist_tracks",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id", ondelete = "CASCADE"), primary_key = True),
    Column("track_id",    Integer, ForeignKey("tracks.id",    ondelete = "CASCADE"), primary_key = True),
    Column("position",    Integer, nullable = False)
)

# NORMAL TABLES
class User(Base):
    __tablename__ = "users"

    id:            Mapped[int]              = mapped_column(Integer,  primary_key = True,  autoincrement = True)
    username:      Mapped[str]              = mapped_column(String(255), nullable = False, unique = True, index = True)
    created_at:    Mapped[datetime]         = mapped_column(DateTime,    nullable = False, default = utc_now)
    password_hash: Mapped[str]              = mapped_column(String(255), nullable = False)
    tracks:        Mapped[list["Track"]]    = relationship("Track",    back_populates = "added_by", cascade = "all, delete-orphan")
    sessions:      Mapped[list["Session"]]  = relationship("Session",  back_populates = "user",     cascade = "all, delete-orphan")
    playlists:     Mapped[list["Playlist"]] = relationship("Playlist", back_populates = "owner",    cascade = "all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
class Session(Base):
    __tablename__ = "sessions"
    
    id:         Mapped[int]      = mapped_column(Integer, primary_key = True,  autoincrement = True)
    token:      Mapped[str]      = mapped_column(String(36), nullable = False, unique = True, index = True) # UUID
    created_at: Mapped[datetime] = mapped_column(DateTime,   nullable = False, default = utc_now)
    expires_at: Mapped[datetime] = mapped_column(DateTime,   nullable = False)
    user_id:    Mapped[int]      = mapped_column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    user:       Mapped["User"]   = relationship("User", back_populates = "sessions")
    
    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"

class Artist(Base):
    __tablename__ = "artists"

    id:     Mapped[int]           = mapped_column(Integer,  primary_key = True, autoincrement = True)
    name:   Mapped[str]           = mapped_column(String(255), nullable = False, unique = True, index = True)
    tracks: Mapped[list["Track"]] = relationship("Track", back_populates = "artists", secondary = track_artists)
    albums: Mapped[list["Album"]] = relationship("Album", back_populates="album_artist")
    
    def __repr__(self):
        return f"<Artist(id={self.id}, name='{self.name}')>"
    
class Album(Base):
    __tablename__ = "albums"
    
    id:              Mapped[int]                = mapped_column(Integer,  primary_key = True, autoincrement = True)
    title:           Mapped[str]                = mapped_column(String(255), nullable = False, index = True)
    release_date:    Mapped[Optional[datetime]] = mapped_column(DateTime,    nullable = True)
    album_artist_id: Mapped[Optional[int]]      = mapped_column(Integer, ForeignKey("artists.id", ondelete = "SET NULL"), nullable = True)
    album_artist:    Mapped[Optional["Artist"]] = relationship("Artist", back_populates = "albums")
    tracks:          Mapped[list["Track"]]      = relationship("Track",  back_populates = "album", cascade = "all, delete-orphan")
    
    def __repr__(self):
        return f"<Album(id={self.id}, title='{self.title}')>"

class Track(Base):
    __tablename__ = "tracks"
    
    id:               Mapped[int]               = mapped_column(Integer,  primary_key = True, autoincrement = True)
    title:            Mapped[str]               = mapped_column(String(255), nullable = False, index = True)
    lyrics:           Mapped[Optional[str]]     = mapped_column(Text,        nullable = True)
    duration:         Mapped[float]             = mapped_column(Float,       nullable = False) # seconds
    file_path:        Mapped[str]               = mapped_column(String(512), nullable = False) # original path
    opus_path:        Mapped[str]               = mapped_column(String(512), nullable = False) # usable path
    added_date:       Mapped[datetime]          = mapped_column(DateTime,    nullable = False, default = utc_now)
    track_number:     Mapped[Optional[int]]     = mapped_column(Integer,     nullable = True)
    needs_review:     Mapped[bool]              = mapped_column(Boolean,     nullable = False, default = False)
    cover_art_path:   Mapped[Optional[str]]     = mapped_column(String(512), nullable = True) # keep null
    added_by_user_id: Mapped[int]               = mapped_column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    album_id:         Mapped[Optional[int]]     = mapped_column(Integer, ForeignKey("albums.id", ondelete = "SET NULL"), nullable = True)
    jobs:             Mapped[list["Job"]]       = relationship("Job",    back_populates = "track", cascade = "all, delete-orphan")
    album:            Mapped[Optional["Album"]] = relationship("Album",  back_populates = "tracks")
    genres:           Mapped[list["Genre"]]     = relationship("Genre",  back_populates = "tracks", secondary = track_genres)
    artists:          Mapped[list["Artist"]]    = relationship("Artist", back_populates = "tracks", secondary = track_artists)
    added_by:         Mapped["User"]            = relationship("User",   back_populates = "tracks")
    
    def __repr__(self):
        return f"<Track(id={self.id}, title='{self.title}', duration={self.duration})>"

class Genre(Base):
    __tablename__ = "genres"
    
    id:     Mapped[int]           = mapped_column(Integer,  primary_key = True, autoincrement = True)
    name:   Mapped[str]           = mapped_column(String(100), nullable = False, unique = True, index = True)
    tracks: Mapped[list["Track"]] = relationship("Track", secondary = track_genres, back_populates = "genres")
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

class Playlist(Base):
    __tablename__ = "playlists"
    
    id:         Mapped[int]           = mapped_column(Integer,  primary_key = True, autoincrement = True)
    name:       Mapped[str]           = mapped_column(String(255), nullable = False)
    is_public:  Mapped[bool]          = mapped_column(Boolean,     nullable = False, default = False)
    created_at: Mapped[datetime]      = mapped_column(DateTime,    nullable = False, default = utc_now)
    user_id:    Mapped[int]           = mapped_column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    owner:      Mapped["User"]        = relationship("User",  back_populates = "playlists")
    tracks:     Mapped[list["Track"]] = relationship("Track", back_populates = None, secondary = playlist_tracks)
    
    def __repr__(self):
        return f"<Playlist(id={self.id}, name='{self.name}', is_public={self.is_public})>"

class Job(Base): # ooooooo spooopy
    __tablename__ = "jobs"
    
    id:            Mapped[int]                = mapped_column(Integer, primary_key = True, autoincrement = True)
    type:          Mapped[str]                = mapped_column(String(50), nullable = False) # "transcode", "fingerprint", etc
    status:        Mapped[str]                = mapped_column(String(50), nullable = False, default = "pending") # "pending", "running", "complete", "failed"
    created_at:    Mapped[datetime]           = mapped_column(DateTime,   nullable = False, default = utc_now)
    started_at:    Mapped[Optional[datetime]] = mapped_column(DateTime,   nullable = True)
    completed_at:  Mapped[Optional[datetime]] = mapped_column(DateTime,   nullable = True)
    error_message: Mapped[Optional[str]]      = mapped_column(Text,       nullable = True)
    track_id:      Mapped[Optional[int]]      = mapped_column(Integer, ForeignKey("tracks.id", ondelete = "CASCADE"))
    track: Mapped[Optional[int]]              = relationship("Track", back_populates = "jobs")
    
    def __repr__(self):
        return f"<Job(id={self.id}, type='{self.type}', status='{self.status}')>"