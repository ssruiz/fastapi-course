from datetime import datetime

from models import State
from schemas.base import ComplaintBase


class ComplaintOut(ComplaintBase):
    created_at: datetime
    status: State

    class Config:
        orm_mode = True
