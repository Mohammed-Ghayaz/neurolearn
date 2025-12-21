from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from ..db.database import Base
from uuid import uuid4


class Subtopic(Base):
    __tablename__="subtopics"
    __table_args__ = (UniqueConstraint("topic_id", "order_index"))
    
    subtopic_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.topic_id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)