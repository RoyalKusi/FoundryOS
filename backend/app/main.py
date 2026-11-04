"""FastAPI app factory — the Core API."""

from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.errors import register_exception_handlers

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    settings = get_settings()
    logger.info("startup", env=settings.app_env, llm_mode=settings.llm_mode)
    yield
    logger.info("shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="FoundryOS Core API",
        version="0.1.0",
        description="Company Operating System — multi-tenant, agent runtime, RAG",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "env": settings.app_env,
            "llm_mode": settings.llm_mode,
            "baseten_base_url": settings.baseten_base_url,
            "baseten_reasoning_model": settings.baseten_reasoning_model,
            "baseten_fast_model": settings.baseten_fast_model,
            "baseten_key_configured": "true" if settings.baseten_api_key else "false",
        }

    @app.get("/", tags=["ops"])
    async def root() -> JSONResponse:
        return JSONResponse(
            {
                "name": "FoundryOS Core API",
                "version": "0.1.0",
                "docs": "/docs",
                "health": "/health",
            }
        )

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
