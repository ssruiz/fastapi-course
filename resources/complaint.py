from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from managers.auth import oauth_scheme
from managers.complaint import ComplaintManager
from models import User
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from services.session import get_db, get_request_user

router = APIRouter(tags=["Complaint"], prefix="/complaint")


@router.get("", status_code=200, dependencies=[Depends(oauth_scheme)], response_model=List[ComplaintOut])
async def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_request_user)):
    complaints = ComplaintManager.get_complaints(current_user, db)
    return complaints


@router.post("", dependencies=[Depends(oauth_scheme)], response_model=ComplaintOut, status_code=201)
async def create(complaint_data: ComplaintIn, db: Session = Depends(get_db),
                 current_user: User = Depends(get_request_user)):
    complaint = ComplaintManager.create_complaint(complaint_data, current_user.id, db)
    return complaint
