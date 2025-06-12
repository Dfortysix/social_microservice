from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.db import get_db
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.PostOut)
async def create(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return await crud.create_post(db, post, author_id=user_id)

@router.get("/", response_model=list[schemas.PostOut])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db)

@router.get("/{post_id}", response_model=schemas.PostOut)
async def get(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
async def update(post_id: int, update_data: schemas.PostUpdate, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await crud.update_post(db, db_post, update_data)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.delete_post(db, db_post)
