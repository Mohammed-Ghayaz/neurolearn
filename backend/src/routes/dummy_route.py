from fastapi import APIRouter, Depends
from ..dependencies.auth_dependency import require_parent, require_student
from ..models.user_model import User
from ..db.database import get_db

router = APIRouter()

@router.get("/dummy")
def dummy_route(db=Depends(get_db)):
    return {"db": "connected"}

@router.get("/parent-only")
def dummy_parent_route(current_user: User = Depends(require_parent)):
    return {"message": "Parent View"}

@router.get("/student-only")
def dummy_student_route(current_user: User = Depends(require_student)):
    return {"message": "Student View"}