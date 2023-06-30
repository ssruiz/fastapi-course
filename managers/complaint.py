from sqlalchemy import select
from sqlalchemy.orm import Session

from models import RoleType, State, Complaint, User
from schemas.request.complaint import ComplaintIn


class ComplaintManager:
    @staticmethod
    def get_complaints(user: User, db: Session):

        q = select(Complaint)

        if user.role == RoleType.complainer:
            q = q.where(Complaint.user_id.__eq__(user.id))
        elif user.role == RoleType.approver:
            q = select(Complaint).filter_by(status=State.pending)

        return db.scalars(q).fetchall()

    @staticmethod
    def create_complaint(complain_data: ComplaintIn, user_id: int, db: Session):
        new_complaint = Complaint(**complain_data.dict(), user_id=user_id)
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        return new_complaint.dict()
