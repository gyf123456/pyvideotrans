"""FastAPI application factory with CORS and lifespan."""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from videotrans.web import progress
from videotrans.web.ws import router as ws_router
from videotrans.web.routes.tasks import router as tasks_router
from videotrans.web.routes.upload import router as upload_router
from videotrans.web.routes.providers import router as providers_router
from videotrans.web.routes.languages import router as languages_router
from videotrans.web.routes.voices import router as voices_router
from videotrans.web.routes.config import router as config_router
from videotrans.web.routes.files import router as files_router
from videotrans.web.routes.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: register WebSocket broadcast bridge
    loop = asyncio.get_running_loop()
    progress.init_bridge(loop)
    yield
    # Shutdown: nothing special needed


def create_app() -> FastAPI:
    app = FastAPI(
        title="pyVideoTrans Web API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — allow all origins for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers
    app.include_router(tasks_router)
    app.include_router(upload_router)
    app.include_router(providers_router)
    app.include_router(languages_router)
    app.include_router(voices_router)
    app.include_router(config_router)
    app.include_router(files_router)
    app.include_router(system_router)
    app.include_router(ws_router)

    # Serve Vue frontend static files (production build)
    dist_dir = Path(__file__).parent.parent.parent / "web" / "dist"
    if dist_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="frontend")

    return app
