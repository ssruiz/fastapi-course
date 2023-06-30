from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from managers.auth import AuthManager
from models import User, RoleType
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

    @staticmethod
    def get_users(db: Session):
        q = select(User)
        users_db = db.scalars(q).all()
        return users_db

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        q = select(User).filter_by(email=email)
        users_db = db.scalars(q).all()
        return users_db

    @staticmethod
    def change_role(new_role: RoleType, user_id: int, db: Session):
        user_db = db.get(User, user_id)
        if not user_db:
            raise HTTPException(404, "User not found")

        user_db.role = new_role
        db.commit()
        db.refresh(user_db)
        return user_db
