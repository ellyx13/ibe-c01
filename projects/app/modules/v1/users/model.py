from pydantic import BaseModel
from typing import Optional


class Users(BaseModel):
    fullname: str
    email: str
    phone_number: Optional[str] = None
    password: str