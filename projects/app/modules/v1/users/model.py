from pydantic import BaseModel
from typing import Optional, Literal


class Users(BaseModel):
    fullname: str
    email: str
    phone_number: Optional[str] = None
    password: str
    type: Literal["user", "admin"]