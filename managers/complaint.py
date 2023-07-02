import os.path
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from constants import TEMP_FILE_FOLDER
from models import RoleType, State, Complaint, User
from schemas.request.complaint import ComplaintIn
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo

s3 = S3Service()
ses = SESService()


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
        complain_data_dict = complain_data.dict()
        encoded_photo = complain_data_dict.pop("encoded_photo")
        extension = complain_data_dict.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        uploaded_photo_url = s3.upload(path, name, extension)
        os.remove(path)
        new_complaint = Complaint(**complain_data_dict, user_id=user_id, photo_url=uploaded_photo_url)
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        return new_complaint.dict()

    @staticmethod
    def delete_complaint(complaint_id: int, user_id: int, db: Session):
        complaint_to_delete = db.get(Complaint, complaint_id)
        db.delete(complaint_to_delete)
        db.commit()

    @staticmethod
    def change_status(complaint_id: int, new_state: State, db: Session):
        complaint_to_delete = db.get(Complaint, complaint_id)
        complaint_to_delete.status = new_state
        db.commit()
        ses.send_mail(f"Complaint has been: {new_state.name.capitalize()}", ["ssruiz6@gmail.com"],
                      f"The new status of your complaint is: {new_state.name.capitalize()}")
