from ..utils.jwt import verify_access_token
from uuid import UUID
from ..models.user_model import User
from sqlalchemy.orm import Session
from ..db.database import get_db
from fastapi import Depends, HTTPException, Header

def get_token_from_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    return authorization.split(" ", 1)[1]

def get_current_user(db: Session = Depends(get_db), jwt_token: str = Depends(get_token_from_header)):
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Unauthorized user")

    payload = verify_access_token(jwt_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized user")

    user = db.query(User).filter_by(user_id=UUID(payload.user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized user")

    return user