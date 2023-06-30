from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from managers.auth import AuthManager
from models import User
from schemas.request.user import UserRegisterIn, UserLoginIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    def register(user_data: UserRegisterIn, db: Session):

        user_data.password = pwd_context.hash(user_data.password)
        try:
            new_user = User(**user_data.dict())
            db.add(new_user)
            db.commit()
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")

        db.refresh(new_user)
        return AuthManager.encode_token(new_user)

    @staticmethod
    def login(user_data: UserLoginIn, db: Session):
        q = select(User).filter_by(email=user_data.email)
        user_db: User = db.scalar(q)
        if not user_db:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data.password, user_db.password):
            raise HTTPException(400, "Wrong email or password")

        return AuthManager.encode_token(user_db)
