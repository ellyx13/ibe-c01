from fastapi import APIRouter

from . import schemas
from . import services


router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("/register", status_code=201, response_model=schemas.RegisterUserResponse)
async def register(data: schemas.RegisterUserRequest):
    data = data.model_dump()
    result = await services.register_user(data)
    return schemas.RegisterUserResponse(**result) 


@router.post("/login", status_code=201, response_model=schemas.LoginUserResponse, responses= {
                420: {"model": schemas.ErrorResponse, "description": "User not found"}, 
                421: {"model": schemas.ErrorResponse, "description": "Password not match"}, 
                })
async def login(data: schemas.LoginUserRequest):
    data = data.model_dump()
    result = await services.login_user(data)
    return schemas.LoginUserResponse(**result) 


@router.get("/me", status_code=200, response_model=schemas.GetMeResponse, responses= {
                423: {"model": schemas.ErrorResponse, "description": "Database is empty"}, 
                })
async def get_me():
    result = await services.get_me()
    return schemas.GetMeResponse(**result) 

@router.put("/me", status_code=200, response_model=schemas.UpdateMeResponse, responses= {
                423: {"model": schemas.ErrorResponse, "description": "Database is empty"}, 
                })
async def update_me(data: schemas.UpdateMeRequest):
    data = data.model_dump(exclude_none=True)
    result = await services.update_me(data)
    return schemas.UpdateMeResponse(**result) 

@router.delete("/me", status_code=204)
async def delete_me():
    await services.delete_me()