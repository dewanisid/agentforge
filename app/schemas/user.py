from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    