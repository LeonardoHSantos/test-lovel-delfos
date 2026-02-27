from __future__ import annotations

from fastapi import FastAPI

from src.source_api.routes import router as data_router


def create_app() -> FastAPI:
    app = FastAPI(title="Energy Source Data API")
    app.include_router(data_router)
    return app


app = create_app()

