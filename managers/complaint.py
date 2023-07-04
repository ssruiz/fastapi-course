import os.path
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from constants import TEMP_FILE_FOLDER
from models import RoleType, State, Complaint, User, Transaction
from schemas.request.complaint import ComplaintIn
from services.s3 import S3Service
from services.ses import SESService
from services.wise import WiseService
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
    def create_complaint(complain_data: ComplaintIn, user: User, db: Session):
        try:

            complain_data_dict = complain_data.dict()
            encoded_photo = complain_data_dict.pop("encoded_photo")
            extension = complain_data_dict.pop("extension")
            name = f"{uuid.uuid4()}.{extension}"
            path = os.path.join(TEMP_FILE_FOLDER, name)
            decode_photo(path, encoded_photo)
            uploaded_photo_url = s3.upload(path, name, extension)
            os.remove(path)
            new_complaint = Complaint(**complain_data_dict, user_id=user.id, photo_url=uploaded_photo_url)
            db.add(new_complaint)
            db.flush()
            db.refresh(new_complaint)
            ComplaintManager.issue_transaction(complain_data.amount, f"{user.first_name} {user.last_name}",
                                               user.iban,
                                               new_complaint.id,
                                               db
                                               )
            return new_complaint.dict()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.commit()

    @staticmethod
    def delete_complaint(complaint_id: int, user_id: int, db: Session):
        complaint_to_delete = db.get(Complaint, complaint_id)
        db.delete(complaint_to_delete)
        db.commit()

    @staticmethod
    def change_status(complaint_id: int, new_state: State, db: Session):
        nested = db.begin_nested()
        try:
            complaint_to_change = db.get(Complaint, complaint_id)
            complaint_to_change.status = new_state
            wise = WiseService()
            q = select(Transaction).where(Transaction.complaint_id.__eq__(complaint_to_change.id))
            transaction: Transaction = db.scalar(q).e
            if new_state.name == State.approved.name:
                wise.fund_transfer(transaction.transfer_id)
            else:
                wise.cancel_transfer(transaction.transfer_id)
                print("Cancel")

            ses.send_mail(f"Complaint has been: {new_state.name.capitalize()}", ["ssruiz6@gmail.com"],
                          f"The new status of your complaint is: {new_state.name.capitalize()}")
        except Exception as e:
            nested.rollback()
            raise e
        finally:
            nested.commit()

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id, db: Session):
        # DE89370400440532013000
        wise = WiseService()
        quote_id_ = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(full_name, iban)
        transfer_ = wise.create_transfer(recipient_id["id"], quote_id_["id"])
        # res = wise.fund_transfer(transfer_["id"])
        data = {
            "quote_id": quote_id_["id"],
            "transfer_id": transfer_["id"],
            "recipient_id": str(recipient_id["id"]),
            "target_account_id": str(recipient_id["id"]),
            "amount": amount,
            "complaint_id": complaint_id
        }
        new_transaction = Transaction(**data)
        db.add(new_transaction)
        db.flush()
        db.refresh(new_transaction)
        return new_transaction.dict()
