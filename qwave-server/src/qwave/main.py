import sys
import uvicorn

from pathlib import Path
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware

from qwave.config import load_config, get_config
from qwave.cli.init import prompt_box
from qwave.database import init_db, create_tables
# from qwave.workers.worker import start_worker, stop_worker

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
        docs_url = None, redoc_url = None
    )
    
    app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name = "static")
    
    app.add_middleware(
        CORSMiddleware,
        # FIXME: THIS IS NOT SECURE FOR PUBLIC EXPOSURE
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )
    
    @app.get("/", tags = ["root"], include_in_schema = False)
    def read_root(): # TODO: This is where the webapp client links in
        config = get_config()
        return {
            "message": "qWave is running!",
            "server_name": config.server_name,
            "version": version("qwave"),
        }
        
    @app.get("/health", tags = ["root"])
    def health_check():
        return {"status": "healthy"} # TODO: lmao what if it's not
        
    @app.get("/docs")
    def get_docs() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url = app.openapi_url,
            title = "qWave API",
            swagger_favicon_url = "/static/favicon.png")
    
    # TODO: ADD ALL THE ROUTERS HERE
    # app.include_router(bnuuy.router, prefix = "/bnuuy", tags = ["bnuuy"])
    
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