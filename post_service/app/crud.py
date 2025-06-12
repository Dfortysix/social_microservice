from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

async def create_post(db: AsyncSession, post: schemas.PostCreate, author_id: int):
    db_post = models.Post(**post.dict(), author_id=author_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    return result.scalar_one_or_none()

async def get_posts(db: AsyncSession):
    result = await db.execute(select(models.Post))
    return result.scalars().all()

async def update_post(db: AsyncSession, db_post: models.Post, updates: schemas.PostUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, db_post: models.Post):
    await db.delete(db_post)
    await db.commit()
