import sys
import uvicorn

from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager

from qwave.config import load_config, get_config
from qwave.cli.init import prompt_box
from qwave.database import init_db, create_tables
from importlib.metadata import version
# from qwave.workers.worker import start_worker, stop_worker
from fastapi.middleware.cors import CORSMiddleware

# from qwave.api import ...
# TODO: add workers and routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # FIXME: add color codes from config and stylize
    print("[INFO] Starting qWave...")
    print("[INFO] Loading config...")
    try:
        config = load_config()
        print(f"[SUCCESS] Config loaded from {config.music_dir.parent / 'qwave.ini'}")
    except Exception as e:
        print(f"[ERROR] {e}\nTry running qwave_init?")
        sys.exit(1)
    
    print("[INFO] Connecting to database...")
    try:
        init_db()
        print(f"[SUCCESS] Database connected: {config.database_url}")
    except Exception as e:
        print(f"[ERROR] Failed to init database: {e}")
        sys.exit(0)
    print("[INFO] Starting worker...")
    # TODO: start_worker()
    print("[INFO] Worker started")
    
    prompt_box(f"Server '{config.server_name}' started!", [
        f"Listening on: http://{config.host}:{config.port}",
        f"API docs: http://{config.host}:{config.port}/docs",
        f"Output directory: {config.music_dir}"
    ], cls = False)
    
    yield
    
    print("======================================")
    print("[INFO] Shutting down!!")
    print("[INFO] Stopping worker...")
    # TODO: stop_worker()
    print("[SUCCESS] Worker stopped!")
    print("[SUCCESS] goodbye!")
        
        
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