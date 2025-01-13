from fastapi import HTTPException
import bcrypt
from . import schemas
from . import model
from db.crud import BaseCRUD
from db.config import DATABASE_URL, DATABASE_NAME
from modules.v1.auth.services import create_access_token
from datetime import datetime
from . import config

user_crud = BaseCRUD(database_url=DATABASE_URL, database_name=DATABASE_NAME, collection_name="users")


async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

async def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

async def register_user(data: schemas.RegisterUserRequest, is_create_admin: bool = False) -> model.Users:
    if await get_by_email(email=data['email']) is not None:
        raise HTTPException(409, detail="User have this email already exists")
    data["password"] = await hash_password(data["password"])
    data["type"] = "user" if is_create_admin is False else "admin"
    data["created_at"] = datetime.now()
    user = model.Users(**data).model_dump()
    user_id = await user_crud.save(user)
    result =  await user_crud.get_by_id(_id=user_id)
    result['token_type'] = "Bearer"
    result['access_token'] = await create_access_token(user_id=user_id)
    return result

async def create_default_admin():
    if await get_by_email(email=config.ADMIN_EMAIL_DEFAULT) is not None:
        return
    data = {}
    data['fullname'] = config.ADMIN_FULLNAME_DEFAULT
    data['email'] = config.ADMIN_EMAIL_DEFAULT
    data['password'] = config.ADMIN_PASSWORD_DEFAULT
    return await register_user(data=data, is_create_admin=True)

async def get_by_email(email: str) -> model.Users:
    users = await user_crud.get_by_field(field="email", value=email)
    if users:
        return users[0]
    return None

async def login_user(data: schemas.LoginUserRequest) -> model.Users:
    user = await get_by_email(data['email'])
    if user is None:
        raise HTTPException(420, detail="User not found")
        
    if await check_password(data['password'], user['password']) is False:
        raise HTTPException(421, detail="Password not match")
    user['token_type'] = "Bearer"
    user['access_token'] = await create_access_token(user_id=user['_id'])
    return user

async def get_me(user_id: str) -> model.Users:
    return await user_crud.get_by_id(_id=user_id)

async def check_modified(data: dict, users: model.Users) -> bool:
    for key, value in data.items():
        if users[key] != value:
            return True
    return False


async def update_me(data: schemas.UpdateMeRequest, current_user: str) -> model.Users:
    user = await get_me(user_id=current_user)
    if not await check_modified(data=data, users=user):
        raise HTTPException(304, detail="No data is modified")
    data['updated_at'] = datetime.now()
    await user_crud.update_by_id(_id=current_user, new_data=data)
    return await user_crud.get_by_id(_id=current_user)

async def delete_me(current_user: str):
    user = await get_me(user_id=current_user)
    if user is None:
        raise HTTPException(404, detail="User not found")
    await user_crud.delete_by_id(_id=current_user)

async def is_admin(user_id: str) -> bool:
    user = await get_me(user_id=user_id)
    if user['type'] == "admin":
        return True
    return False