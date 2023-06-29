from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select

from db import LocalSession
from managers.auth import AuthManager
from models import user, User
from schemas.request.user import UserRegisterIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data: UserRegisterIn):
        with LocalSession() as session:
            user_data.password = pwd_context.hash(user_data.password)
            try:
                new_user = User(**user_data.dict())
                _id = session.add(new_user)
                session.commit()
            except UniqueViolationError:
                raise HTTPException(400, "User with this email already exists")

            session.refresh(new_user)
            return AuthManager.encode_token(new_user)

    @staticmethod
    async def login(user_data: UserRegisterIn):
        with LocalSession() as session:
            q = select(User).filter_by(email=user_data.email)
            user_db: User = session.scalar(q)
            if not user_db:
                raise HTTPException(400, "Wrong email or password")
            elif not pwd_context.verify(user_data.password, user_db.password):
                raise HTTPException(400, "Wrong email or password")

            return AuthManager.encode_token(user_db)
