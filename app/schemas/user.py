from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False  # Added this for your admin check logic

class UserCreate(UserBase):
    password: str  

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True