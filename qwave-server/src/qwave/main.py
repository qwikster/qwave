import sys
import uvicorn

from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager

from qwave.config import load_config, get_config
from qwave.database import init_db, create_tables
from importlib.metadata import version
# from qwave.workers.worker import start_worker, stop_worker
from fastapi.middleware.cors import CORSMiddleware

# from qwave.api import ...
# TODO: add workers and routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # FIXME: add color codes from config and stylize
    print("Starting server...")
    # ...
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title =       "qWave",
        description = "Lightweight audio-only media server",
        version =     version("qwave"),
        lifespan =    lifespan,
        docs_url =    "/docs",
        redoc_url=    "/redoc",
    )
    
    # TODO: CORS, root endpoint, /health, routers
    
    return app

def entry():
    load_config()
    app = create_app()
    config = get_config()
    
    uvicorn.run(
        app,
        host = config.host,
        port = config.port,
        log_level = "info"
    )

if __name__ == "__main__":
    entry()