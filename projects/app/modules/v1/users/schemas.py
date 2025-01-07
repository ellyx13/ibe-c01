from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str

class RegisterUserRequest(BaseModel):
    fullname: str
    email: str
    password: str
    
class RegisterUserResponse(BaseModel):
    fullname: str
    email: str
    phone_number: Optional[str] = None
    password: str
    
    
class LoginUserRequest(BaseModel):
    email: str
    password: str
    
class LoginUserResponse(RegisterUserResponse):
    pass

class GetMeResponse(RegisterUserResponse):
    pass

class UpdateMeRequest(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    
class UpdateMeResponse(RegisterUserResponse):
    pass