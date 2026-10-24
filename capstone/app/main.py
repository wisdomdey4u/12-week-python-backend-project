from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import Settings
from app.database import Base
from app.routers import auth, workspaces


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()
    engine = create_async_engine(app_settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        application.state.session_factory = session_factory
        application.state.jwt_secret_key = app_settings.jwt_secret_key
        application.state.access_token_minutes = app_settings.access_token_minutes
        yield
        await engine.dispose()

    application = FastAPI(
        title="Learning Hub API",
        description="A multi-tenant learning resource API built in public.",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(auth.router)
    application.include_router(workspaces.router)

    @application.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
