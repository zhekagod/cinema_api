from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.db_models.user import User
from src.schemas.user import UserCreate, UserResponse


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/sign-up", response_model=UserResponse)
def sign_up(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    new_user = User(
        username=user.username,
        password=user.password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user