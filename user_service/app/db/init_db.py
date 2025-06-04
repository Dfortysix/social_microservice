# app/db/init_db.py
import asyncio
from app.db.session import engine
from app.db.base import Base
from app.db.models import User  # Đảm bảo import model để Base biết

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
