from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps

from app.db.session import get_db
from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.api.deps import get_current_user
from app.schemas.token import Token

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # 2. Use the hash function from app.core.security
    hashed_pwd = security.get_password_hash(user_in.password)
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:

    # 1. Try to find the user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Verify the user exists AND the password matches
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Create the Key Card (JWT)
    access_token = security.create_access_token(subject=user.email) 
    refresh_token = security.create_refresh_token(subject=user.email)

    # 4. Return the Token to the user
    return {
       "access_token": access_token,
        "refresh_token": refresh_token, 
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_token: str, 
    db: Session = Depends(deps.get_db)
):
   pass

