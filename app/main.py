"""Application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.models import possession  # noqa: F401 - registers ORM table
from app.routers.possessions import router as possessions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Appropriate for the initial local prototype; introduce migrations when evolving the schema.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Belongings Collection",
    description="A local-first digital library of physical possessions.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(possessions_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
