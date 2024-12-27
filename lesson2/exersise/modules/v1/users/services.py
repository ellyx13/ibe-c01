from fastapi import HTTPException
from . import schemas
from . import model

fake_db = []

async def register_user(data: schemas.RegisterUserRequest) -> model.Users:
    user = model.Users(**data).model_dump()
    fake_db.append(user)
    return user

async def get_by_email(email: str) -> model.Users:
    for user in fake_db:
        if user['email'] == email:
            return user
    return None

async def login_user(data: schemas.LoginUserRequest) -> model.Users:
    user = await get_by_email(data['email'])
    if user is None:
        raise HTTPException(420, detail="User not found")
        
    if user['password'] != data['password']:
        raise HTTPException(421, detail="Password not match")

    return user 

async def get_me() -> model.Users:
    if len(fake_db) == 0:
        raise HTTPException(423, detail="Database is empty")
    return fake_db[0]

async def check_modified(data: dict, users: model.Users) -> bool:
    for key, value in data.items():
        if users[key] != value:
            return True
    return False

async def update_me(data: schemas.UpdateMeRequest) -> model.Users:
    user = await get_me()
    is_modified = await check_modified(data, user)
    if is_modified is False:
        raise HTTPException(304, detail="No data is modified")
    user.update(data)
    fake_db[0] = user
    return user

async def delete_me():
    await get_me()
    fake_db.clear()