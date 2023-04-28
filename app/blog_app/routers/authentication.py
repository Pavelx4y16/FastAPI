from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog_app.JWToken import create_access_token
from blog_app.database import get_db
from blog_app.hashing import Hash
from blog_app.repository import user as user_utils

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_utils.get_by_email(email=request.username, db=db)

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
