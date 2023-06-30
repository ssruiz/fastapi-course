from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from managers.auth import oauth_scheme, is_complainer, is_admin
from managers.complaint import ComplaintManager
from managers.user import UserManager
from models import User, RoleType
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from schemas.response.user import UserOut
from services.session import get_db, get_request_user

router = APIRouter(tags=["Users"], prefix="/users", dependencies=[Depends(oauth_scheme)])


@router.get("", dependencies=[Depends(is_admin)], response_model=List[UserOut], status_code=200)
async def get_user(email: Optional[str] = None, db: Session = Depends(get_db)):
    if email:
        return UserManager.get_user_by_email(email, db)

    return UserManager.get_users(db)


@router.put("/change_role/{user_id}", dependencies=[Depends(is_admin)], response_model=UserOut, status_code=200)
async def change_role(user_id: int, role: RoleType = None, db: Session = Depends(get_db)):
    return UserManager.change_role(role, user_id, db)
