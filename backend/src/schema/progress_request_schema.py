from uuid import UUID
from pydantic import BaseModel

class ProgressRequest(BaseModel):
    session_id: UUID
    progress_percent: float