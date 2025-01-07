from pydantic import BaseModel, Field
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str

class RegisterUserRequest(BaseModel):
    fullname: str
    email: str
    password: str
    
class Response(BaseModel):
    id: str = Field(alias="_id")
    fullname: str
    email: str
    phone_number: Optional[str] = None
    password: str
    type: str

class RegisterUserResponse(Response):
    token_type: str
    access_token: str
    
class LoginUserRequest(BaseModel):
    email: str
    password: str
    
class LoginUserResponse(RegisterUserResponse):
    pass

class GetMeResponse(Response):
    pass

class UpdateMeRequest(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    
class UpdateMeResponse(Response):
    pass