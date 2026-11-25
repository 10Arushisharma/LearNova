from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.db.session import engine
from app.models import Base
from app.api.v1.router import api_router
from app.db.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(debug=settings.DEBUG)
    logger.info("Starting Learnova API — %s", settings.ENVIRONMENT)
    # Create all tables (auto-migrate for SQLite dev; use Alembic for Postgres prod)
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        seed_database(db)
    logger.info("Database ready and seeded.")
    yield
    logger.info("Learnova API shutting down.")


app = FastAPI(
    title="Learnova API",
    description="AI-powered gamified learning platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENVIRONMENT}
