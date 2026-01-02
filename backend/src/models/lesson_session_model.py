from sqlalchemy import Column, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from ..db.database import Base
from uuid import uuid4
from datetime import datetime, timezone

class LessonSession(Base):
    __tablename__ = "lesson_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.lesson_id"), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), index=True, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)
    progress_percent = Column(Float, nullable=False)
    completed = Column(Boolean, default=False)
