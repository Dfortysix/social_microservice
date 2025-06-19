from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load .env từ thư mục gốc của project
env_path = Path(__file__).parents[1] / '.env'
logger.info(f"Loading .env from: {env_path}")
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    logger.info("Loaded .env file successfully")
else:
    logger.warning(f".env file not found at {env_path}")
1
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info(f"USER_SERVICE_URL: {USER_SERVICE_URL}")
logger.info(f"DATABASE_URL: {DATABASE_URL}")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{USER_SERVICE_URL}/users/login")

class TokenData(BaseModel):
    user_id: int

async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info(f"Token: {token}")
        logger.info(f"SECRET_KEY: {SECRET_KEY}")
        logger.info(f"ALGORITHM: {ALGORITHM}")  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            logger.error("User ID is None")
            raise credentials_exception
        logger.info(f"Successfully decoded user_id: {user_id}")
        return int(user_id)
    except JWTError as e:
        logger.error(f"JWT validation failed: {str(e)}")
        raise credentials_exception
