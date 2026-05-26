from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserResponse

from src.db_models.user import User
from src.database import get_db
from src.auth.jwt import create_access_token


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



@auth_router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}