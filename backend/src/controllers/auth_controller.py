from ..schema.auth_schema import RegisterUserRequest, LoginUserRequest
from ..models.user_model import User, UserRole
from sqlalchemy.orm import Session
from ..utils.hash_password import hash_password, verify_password
from ..utils.jwt import create_access_token

def register_user(user_data: RegisterUserRequest, db: Session):
    user = db.query(User).filter_by(email=user_data.email).first()
    if user:
        raise ValueError("User already exists")

    hashed_password = hash_password(user_data.password)

    new_user = User(name=user_data.name, email=user_data.email, password_hash=hashed_password, age=user_data.age, role=UserRole.STUDENT)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return create_access_token(new_user.user_id, new_user.role)

def login_user(user_data: LoginUserRequest, db: Session):
    existing_user = db.query(User).filter_by(email=user_data.email).first()

    if not existing_user:
        raise ValueError("Incorrect email or password")

    is_password_correct = verify_password(user_data.password, existing_user.password_hash)

    if not is_password_correct:
        raise ValueError("Incorrect email or password")

    return create_access_token(existing_user.user_id, existing_user.role)

    