import sys
import uvicorn

from pathlib import Path
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from qwave.config import load_config, get_config
from qwave.cli.init import prompt_box
from qwave.database import init_db
from qwave.utils.log_item import log_item, clear_log
from qwave.workers.worker import start_worker, stop_worker

from qwave.api import auth, server, artists, genres, albums, tracks, stream, search

@asynccontextmanager
async def lifespan(app: FastAPI):
    clear_log()
    log_item("Starting qWave", "INFO")
    try:
        config = load_config()
        log_item(f"Config loaded from {config.music_dir.parent / 'qwave.ini'}", "SUCCESS")
    except Exception as e:
        log_item(f"{e} - Try running qwave_init?", "ERROR")
        sys.exit(1)

    log_item("Connecting to database...", "INFO")
    try:
        init_db()
        log_item(f"Connected to database {config.database_url}", "SUCCESS")
    except Exception as e:
        log_item(f"Failed to init database: {e}", "ERROR")
        sys.exit(1)
    start_worker()
    log_item("Server started!", "SUCCESS")
    prompt_box(f"Server '{config.server_name}' started!", [
        f"Listening on: http://{config.host}:{config.port}",
        f"API docs: http://{config.host}:{config.port}/docs",
        f"Output directory: {config.music_dir}"
    ], cls = False)

    yield

    log_item("Shutting down...", "WARN")
    stop_worker()
    log_item("goodbye!", "SUCCESS")


def create_app() -> FastAPI:
    app = FastAPI(
        title =       "qWave",
        description = "Lightweight audio-only media server",
        version =     version("qwave"),
        lifespan =    lifespan,
        docs_url = None
    )

    app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name = "static")

    @app.get("/app", tags = ["root"], include_in_schema = False)
    def read_root():
        config = get_config()
        return {
            "message": "qWave is running! Web client at / (root)",
            "server_name": config.server_name,
            "version": version("qwave"),
        }

    app.add_middleware(
        CORSMiddleware,
        # FIX: not safe for public exposure if auth becomes more important
        allow_origins = ["*"],
        allow_credentials = False,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )

    @app.get("/health", tags = ["root"])
    def health_check():
        return {"status": "healthy"} # TODO: lmao what if it's not

    @app.get("/docs")
    def get_docs() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url = app.openapi_url if app.openapi_url is not None else "/openapi.json",
            title = "qWave API",
            swagger_favicon_url = "/static/favicon.png")

    # TODO: ADD ALL THE ROUTERS HERE
    # app.include_router(bnuuy.router, prefix = "/bnuuy", tags = ["bnuuy", "ing"])
    app.include_router(auth.router,    prefix = "/auth",    tags = ["auth"])
    app.include_router(server.router,  prefix = "/server",  tags = ["server"])
    app.include_router(artists.router, prefix = "/artists", tags = ["artists"])
    app.include_router(genres.router,  prefix = "/genres",  tags = ["genres"])
    app.include_router(albums.router,  prefix = "/albums",  tags = ["albums"])
    app.include_router(tracks.router,  prefix = "/tracks",  tags = ["tracks"])
    app.include_router(stream.router,  prefix = "/stream",  tags = ["stream"])
    app.include_router(search.router,  prefix = "/search",  tags = ["search"])

    app.mount("/", StaticFiles(
        directory = Path(__file__).resolve().parent / "static" / "app",
        html = True
    ), name = "app")

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
