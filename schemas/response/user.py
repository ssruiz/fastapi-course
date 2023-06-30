from models import RoleType
from schemas.base import UserBase


class UserOut(UserBase):
    id: int
    last_name: str
    role: RoleType
    first_name: str
    email: str
    phone: str
    iban: str

    class Config:
        orm_mode = True
