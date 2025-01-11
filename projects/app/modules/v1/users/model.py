from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class Users(BaseModel):
    fullname: str
    email: str
    phone_number: Optional[str] = None
    password: str
    type: Literal["user", "admin"]
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None