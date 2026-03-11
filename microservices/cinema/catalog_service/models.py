"""SQLAlchemy models for catalog service."""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    genre: Mapped[str] = mapped_column(String(80), index=True)
    release_year: Mapped[int] = mapped_column(Integer, index=True)
    rating: Mapped[float] = mapped_column(Float, default=0)
