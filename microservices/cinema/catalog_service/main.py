"""FastAPI app for catalog microservice."""

from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Movie
from .subscription_client import is_active_subscription

app = FastAPI(title="Catalog Service", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.execute(select(Movie.id)).first() is None:
            db.add_all(
                [
                    Movie(title="Interstellar", genre="sci-fi", release_year=2014, rating=8.7),
                    Movie(title="The Matrix", genre="sci-fi", release_year=1999, rating=8.5),
                    Movie(title="Inception", genre="thriller", release_year=2010, rating=8.8),
                    Movie(title="Arrival", genre="sci-fi", release_year=2016, rating=7.9),
                ]
            )
            db.commit()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health() -> dict:
    return {"service": "catalog", "status": "ok"}


@app.get("/movies")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    genre: str | None = None,
    q: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    filters = []
    if genre:
        filters.append(Movie.genre == genre)
    if q:
        filters.append(Movie.title.ilike(f"%{q}%"))
    if min_year is not None:
        filters.append(Movie.release_year >= min_year)
    if max_year is not None:
        filters.append(Movie.release_year <= max_year)

    stmt = select(Movie)
    if filters:
        stmt = stmt.where(and_(*filters))
    total = len(db.execute(stmt).scalars().all())
    rows = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return {
        "items": [
            {
                "id": m.id,
                "title": m.title,
                "genre": m.genre,
                "release_year": m.release_year,
                "rating": m.rating,
            }
            for m in rows
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@app.get("/protected/movies")
def list_movies_for_subscriber(user_id: str, db: Session = Depends(get_db)) -> dict:
    try:
        active = is_active_subscription(user_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"subscription dependency unavailable: {exc}") from exc

    if not active:
        raise HTTPException(status_code=403, detail="inactive subscription")
    return list_movies(db=db)
