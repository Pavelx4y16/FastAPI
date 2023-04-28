from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from hashing import Hash
from repository import user as user_utils

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = user_utils.get_by_email(email=request.username, db=db)

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")

    return user
