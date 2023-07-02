from datetime import datetime

from models import State
from schemas.base import ComplaintBase


class ComplaintOut(ComplaintBase):
    created_at: datetime
    status: State
    photo_url: str

    class Config:
        orm_mode = True
