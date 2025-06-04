# app/main.py

from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1 import user

app = FastAPI(
    title="User Service",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "User service is running!"}

app.include_router(user.router)
