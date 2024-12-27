
from fastapi import FastAPI
from modules.v1.users.routers import router as users_router

app = FastAPI()

app.include_router(users_router)    