from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import mapped_column

from models import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = mapped_column(Integer, primary_key=True)
    quote_id = mapped_column(String(120), nullable=False)
    recipient_id = mapped_column(String(120), nullable=False)
    transfer_id = mapped_column(Integer, nullable=False)
    target_account_id = mapped_column(String(120), nullable=False)
    amount = mapped_column(Float, nullable=False)
    complaint_id = mapped_column(ForeignKey("complaints.id"), nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "quote_id": self.quote_id,
            "recipient_id": self.recipient_id,
            "complaint_id": self.complaint_id,
            "amount": self.amount
        }
