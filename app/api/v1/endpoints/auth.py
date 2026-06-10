from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import create_user, get_user_by_email, login_user

from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = await create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await login_user(db, user_data.email, user_data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

@router.get("/me", response_model = UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


