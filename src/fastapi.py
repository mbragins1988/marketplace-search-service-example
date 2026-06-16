from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.infrastructure.persistence.database import (
    create_engine,
    create_session_factory,
)
from src.middleware import TraceMiddleware
from src.presentation.api.dependencies import setup
from src.presentation.api.routes.public import router as public_router
from src.settings import Settings
from src.tracing import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    settings = Settings()

    engine = create_engine(settings)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        setup(settings, session_factory)
        yield

    app = FastAPI(title="Search Service", lifespan=lifespan)
    app.add_middleware(TraceMiddleware)
    app.include_router(public_router)
    return app
