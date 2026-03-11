"""Feature table for ML training/inference."""

from sqlalchemy import Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TaskFeatures(Base):
    __tablename__ = "task_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True, nullable=False)
    title_length: Mapped[int] = mapped_column(Integer, nullable=False)
    description_length: Mapped[int] = mapped_column(Integer, nullable=False)
    hour_of_day_created: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week_created: Mapped[int] = mapped_column(Integer, nullable=False)
    has_due_date: Mapped[bool] = mapped_column(Boolean, nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    team_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_completion_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    was_overdue: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    predicted_completion_time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overdue_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
