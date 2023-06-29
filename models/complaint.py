import datetime
from typing import List

from sqlalchemy import String, Enum, Text, DateTime, func, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models import User
from models.base import Base
from models.enums import State


class Complaint(Base):
    __tablename__ = "complaints"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(120), nullable=False)
    description = mapped_column(Text, nullable=False)
    photo_url = mapped_column(String(200), nullable=False)
    amount = mapped_column(Float, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())
    status = mapped_column(Enum(State), server_default=State.pending.name)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[List["User"]] = relationship(back_populates="complaints")
