from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class ComplaintBase(BaseModel):
    title: str
    description: str
    amount: float
