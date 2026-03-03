"""Task relation graph edges."""

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TaskRelation(Base):
    __tablename__ = "task_relations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True, nullable=False)
    target_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True, nullable=False)
    relation_type: Mapped[str] = mapped_column(
        Enum("blocks", "depends_on", "duplicates", "related_to", "subtask_of", name="relation_type"),
        nullable=False,
    )
