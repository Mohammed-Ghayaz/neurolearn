from fastapi import APIRouter, Depends
from ..dependencies.auth_dependency import get_current_user
from ..models.user_model import User

router = APIRouter()

@router.get("/profile")
def get_user(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }