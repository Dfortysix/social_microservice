from fastapi import FastAPI
from app.api.v1 import post
from app.db import Base, engine

app = FastAPI(title="Post Service")

app.include_router(post.router, prefix="/posts", tags=["posts"])

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
