from sqlalchemy import Column, Text, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from ..db.database import Base
from uuid import uuid4
from datetime import datetime, timezone
from enum import Enum

class MistakeType(str, Enum):
    MISREAD = "misread"
    SKIPPED = "skipped"
    HINT = "hint"

class MistakeEvent(Base):
    __tablename__ = "mistake_events"

    mistake_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("lesson_sessions.session_id"), index=True, nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.lesson_id"), index=True, nullable=False)
    subtopic_id = Column(UUID(as_uuid=True), ForeignKey("subtopics.subtopic_id"), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), index=True, nullable=False)
    mistake_type = Column(SQLAlchemyEnum(MistakeType, native_enum=False), nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
