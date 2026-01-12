from fastapi import APIRouter, Depends
from app.api import deps
from app.models.user import User
from app.schemas.user import UserOut 

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_user_me(
    current_user: User = Depends(deps.get_current_user)
):
    
    return current_user