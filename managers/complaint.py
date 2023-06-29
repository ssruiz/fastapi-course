from db import LocalSession
from models import complaint, RoleType, State, Complaint
from sqlalchemy import select


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        with LocalSession() as session:
            q = select(Complaint)

            if user["role"] == RoleType.complainer:
                q = q.where(Complaint.user_id.__eq__(user["sub"]))
            elif user["role"] == RoleType.approver:
                q = select(Complaint).filter_by(status=State.pending)

            return await session.fetch_all(q)
    #
    # @staticmethod
    # async def create_complaint(complain_data):
    #     id_ = await database.execute(complaint.insert().values(**complain_data))
    #     return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
