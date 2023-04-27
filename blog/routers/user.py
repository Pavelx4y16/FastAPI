from typing import List

import models
import schemas
from database import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["users"])
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def destroy(id: int, db: Session = Depends(get_db)):
    items = db.query(models.User).filter(models.User.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


@router.put('/users/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["users"])
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found.")
    user.update({
        models.User.name: request.name,
        models.User.email: request.email,
        models.User.password: request.password})
    db.commit()

    return 'updated'


@router.get('/users', response_model=List[schemas.ShowUser], tags=["users"])
def user_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found.")
    return user
