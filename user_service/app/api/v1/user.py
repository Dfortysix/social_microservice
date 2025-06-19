from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut, Token
from app.crud.user import get_user_by_email, create_user
from app.db.session import AsyncSessionLocal
from app.services.auth import verify_password, create_access_token
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from fastapi.security import OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("app/.env")
load_dotenv(env_path)

router = APIRouter(prefix="/users", tags=["Users"])

# OAuth2 client setup
config = Config(environ=os.environ)
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_uri': 'http://127.0.0.1:10000/users/auth/google/callback'
    }
)

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, str(user.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(db_user.id), "email": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    request.session.clear()
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    print("Login Step: redirect to Google")
    print("Session state:", request.session.get('state'))
    return response

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    if not user_info:
        raise HTTPException(status_code=400, detail="Google login failed")

    email = user_info["email"]
    existing_user = await get_user_by_email(db, email)

    if not existing_user:
        new_user = UserCreate(email=email, password=os.urandom(16).hex())
        existing_user = await create_user(db, new_user)

    access_token = create_access_token({"sub": str(existing_user.id), "email": existing_user.email})
    response = RedirectResponse(url=f"/docs?token={access_token}")
    return response
