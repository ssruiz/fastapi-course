from typing import List

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from models.base import Base
from .enums import RoleType


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120))
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(120))
    role: Mapped[RoleType] = mapped_column(Enum(RoleType), server_default=RoleType.complainer.name)
    iban: Mapped[str] = mapped_column(String(120))
    complaints = relationship("Complaint", back_populates="user")
