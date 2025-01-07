from fastapi import HTTPException
from . import schemas
from . import model
from db.crud import BaseCRUD
from db.config import DATABASE_URL, DATABASE_NAME


user_crud = BaseCRUD(database_url=DATABASE_URL, database_name=DATABASE_NAME, collection_name="users")

async def register_user(data: schemas.RegisterUserRequest) -> model.Users:
    user = model.Users(**data).model_dump()
    user_id = await user_crud.save(user)
    return await user_crud.get_by_id(_id=user_id)

async def get_by_email(email: str) -> model.Users:
    users = await user_crud.get_by_field(field="email", value=email)
    if users:
        return users[0]
    return None

async def login_user(data: schemas.LoginUserRequest) -> model.Users:
    user = await get_by_email(data['email'])
    if user is None:
        raise HTTPException(420, detail="User not found")
        
    if user['password'] != data['password']:
        raise HTTPException(421, detail="Password not match")

    return user 

async def get_me() -> model.Users:
    pass

async def check_modified(data: dict, users: model.Users) -> bool:
    for key, value in data.items():
        if users[key] != value:
            return True
    return False

async def update_me(data: schemas.UpdateMeRequest) -> model.Users:
    pass

async def delete_me():
    pass