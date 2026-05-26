from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.db_models.user import User


def get_current_user(
    authorization: str = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("user_id="):
        raise HTTPException(status_code=401, detail="Invalid auth format")

    try:
        user_id = int(authorization.split("=")[1])
    except:
        raise HTTPException(status_code=401, detail="Invalid user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user