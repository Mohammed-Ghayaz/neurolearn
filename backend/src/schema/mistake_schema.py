from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from ..models.mistake_event_model import MistakeType

class MistakeEventRequest(BaseModel):
    session_id: UUID
    lesson_id: UUID
    mistake_type: MistakeType
    context: Optional[str] = None
    