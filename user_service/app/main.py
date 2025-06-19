# app/main.py

from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1 import user
import os
from dotenv import load_dotenv
from pathlib import Path
from email.message import EmailMessage
from starlette.middleware.sessions import SessionMiddleware

# Load biến môi trường từ file .env
env_path = Path("app/.env")
load_dotenv(env_path)


allowed_origins = [os.getenv("POST_SERVICE_URL"), os.getenv("USER_SERVICE_URL")]

app = FastAPI(
    title="User Service",
    version="1.0.0",
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# 🔒 Thêm SessionMiddleware (dùng cho OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "your-super-secret-key")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "User service is running!"}

app.include_router(user.router)
