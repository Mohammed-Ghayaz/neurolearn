import jwt
import os
from dotenv import load_dotenv
from uuid import UUID
from models.user_model import UserRole
from typing import Any
from time import time

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET is not set")


def create_access_token(user_id: UUID, role: UserRole) -> str:
    payload = {
        "user_id": user_id,
        "role": role.value,
        "exp": int(time()) + 3600 * 24 * 5
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        raise ValueError(f"An error occurred while verifying the token: {e}")
    