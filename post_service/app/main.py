from fastapi import FastAPI
from app.api.v1 import post
from app.db import Base, engine
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Post Service")

app.include_router(post.router, prefix="/posts", tags=["posts"])

@app.on_event("startup")
async def on_startup():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            existing_tables = [row[0] for row in result]
            
            if not existing_tables:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables created successfully")
            else:
                logger.info(f"Tables already exist: {existing_tables}")
    except Exception as e:
        logger.error(f"Error checking/creating database tables: {str(e)}")
        raise
