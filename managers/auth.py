import jwt
from datetime import datetime, timedelta
from sqlalchemy import select
from fastapi import HTTPException
from starlette.requests import Request
from typing import Optional
from decouple import config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db import LocalSession
from models import User


class AuthManager:
    @staticmethod
    def encode_token(user_data: User):
        try:
            payload = {"sub": user_data.id, "exp": datetime.utcnow() + timedelta(minutes=120)}
            return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
        except Exception as e:
            raise e


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        with LocalSession() as session:
            try:
                payload = jwt.decode(res.credentials, config("JWT_SECRET"), algorithms=["HS256"])
                query = select(User).where(User.id == payload["sub"])
                user_data = session.execute(query).fetchone()
                # user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
                request.state.user = user_data
                return user_data
            except jwt.ExpiredSignatureError:
                raise HTTPException(410, "Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(410, "Invalid token")
