from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    user = User(
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )
    db.add(user)
    await db.flush()
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def login_user(db: AsyncSession, email: str, password: str) -> dict | None:
    user = await authenticate_user(db, email, password)
    if not user:
        return None
    token = create_access_token(data = {"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


