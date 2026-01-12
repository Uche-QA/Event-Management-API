from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None  # User's email or ID (Subject)
    type: Optional[str] = None # To distinguish between 'access' and 'refresh'