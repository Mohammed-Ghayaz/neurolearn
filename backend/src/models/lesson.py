from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, Text, Enum as SQLAlchemyEnum
from ..db.database import Base
from uuid import uuid4
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Lesson(Base):
    __tablename__="lessons"
    __table_args__ = (UniqueConstraint("subtopic_id", "order_index"))

    lesson_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    subtopic_id = Column(UUID(as_uuid=True), ForeignKey("subtopics.subtopic_id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    difficulty = Column(SQLAlchemyEnum(DifficultyLevel, native_enum=False), nullable=False, default=DifficultyLevel.EASY)
    content = Column(Text, nullable=False)
    estimated_time_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)