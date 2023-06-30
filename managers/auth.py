from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from starlette.requests import Request

from db import LocalSession
from models import User, RoleType


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
                user_db: User = session.scalar(query)
                # user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
                request.state.user = user_db
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(410, "Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(410, "Invalid token")


oauth_scheme = CustomHTTPBearer()


def is_admin(request: Request):
    user = request.state.user
    if not user.role == RoleType.admin:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    user = request.state.user
    if not user.role == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_complainer(request: Request):
    user = request.state.user
    if not user.role == RoleType.complainer:
        raise HTTPException(403, "Forbidden")
