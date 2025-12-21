from sqlalchemy.orm import Session
from ..db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from ..controllers.auth_controller import register_user, login_user
from ..schema.auth_schema import RegisterUserRequest, LoginUserRequest

router = APIRouter()

@router.post("/register")
def register_user_router(user_data: RegisterUserRequest, db: Session = Depends(get_db)):
    try:
        jwt_token = register_user(user_data, db)
        return {
            "access_token": jwt_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user_router(user_data: LoginUserRequest, db: Session = Depends(get_db)):
    try:
        jwt_token = login_user(user_data, db)
        return {
            "access_token": jwt_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))