from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from ..db.database import Base
from uuid import uuid4

class Course(Base):
    __tablename__="courses"
    course_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    order_index = Column(Integer, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
