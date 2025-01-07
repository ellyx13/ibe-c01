import jwt
import time
from .config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Request

async def create_access_token(user_id: str, expire_in_minutes: int = 5) -> str:
    data = {}
    data["user_id"] = user_id
    data["exp"] = time.time() + (expire_in_minutes * 60)
    data["iat"] = time.time()
    encoded = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

async def decode_access_token(request: Request) -> str | bool:
    try:
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(401, detail="Unauthorized")
        token = token.split("Bearer ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        time_now = time.time()
        if time_now > decoded["exp"]:
            raise HTTPException(401, detail="Unauthorized")
        return decoded['user_id']
    except Exception:
        raise HTTPException(401, detail="Unauthorized")