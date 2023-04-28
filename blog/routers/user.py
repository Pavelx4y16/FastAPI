from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from repository import user as user_utils

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.get('/', response_model=List[schemas.ShowUser])
def user_list(db: Session = Depends(get_db)):
    return user_utils.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def user_by_id(id: int, db: Session = Depends(get_db)):
    return user_utils.get_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return user_utils.create(request=request, db=db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return user_utils.destroy(id=id, db=db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return user_utils.update(id=id, request=request, db=db)
