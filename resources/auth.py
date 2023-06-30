from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserLoginIn
from services.session import get_db

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=201)
def register(user_data: UserRegisterIn, db: Session = Depends(get_db)):
    token = UserManager.register(user_data, db)
    return {"token": token}


@router.post("/login", status_code=200)
def login(user_data: UserLoginIn, db: Session = Depends(get_db)):
    token = UserManager.login(user_data, db)
    return {"token": token}
