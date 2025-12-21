from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from ..db.database import Base
from uuid import uuid4


class Topic(Base):
    __tablename__="topics"
    __table_args__ = (UniqueConstraint("course_id", "order_index"))
    
    topic_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)