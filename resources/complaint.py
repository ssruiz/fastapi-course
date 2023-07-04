from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from managers.auth import oauth_scheme, is_complainer, is_admin, is_approver
from managers.complaint import ComplaintManager
from models import User, State
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from services.session import get_db, get_request_user

router = APIRouter(tags=["Complaint"], prefix="/complaint", dependencies=[Depends(oauth_scheme)])


@router.get("", status_code=200, response_model=List[ComplaintOut])
async def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_request_user)):
    complaints = ComplaintManager.get_complaints(current_user, db)
    return complaints


@router.post("", dependencies=[Depends(is_complainer)], response_model=ComplaintOut, status_code=201)
async def create(complaint_data: ComplaintIn, db: Session = Depends(get_db),
                 current_user: User = Depends(get_request_user)):
    complaint = ComplaintManager.create_complaint(complaint_data, current_user, db)
    return complaint


@router.delete("/{complaint_id}", dependencies=[Depends(is_admin)], status_code=204)
async def delete(complaint_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_request_user)):
    ComplaintManager.delete_complaint(complaint_id, current_user.id, db)


@router.put("/{complaint_id}/approve", dependencies=[Depends(is_approver)], status_code=204)
async def change(complaint_id: int, db: Session = Depends(get_db)):
    ComplaintManager.change_status(complaint_id, State.approved, db)


@router.put("/{complaint_id}/reject", dependencies=[Depends(is_approver)], status_code=204)
async def change(complaint_id: int, db: Session = Depends(get_db)):
    ComplaintManager.change_status(complaint_id, State.reject, db)
