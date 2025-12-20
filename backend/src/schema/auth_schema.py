from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=8, le=18)