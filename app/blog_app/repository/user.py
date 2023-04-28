from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog_app import models
from blog_app import schemas
from blog_app.hashing import Hash


def get_all(db: Session):
    users = db.query(models.User).all()

    return users


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def destroy(id: int, db: Session):
    items = db.query(models.User).filter(models.User.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


def update(id: int, request: schemas.User, db: Session):
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


def get_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found.")
    return user


def get_by_email(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not found.")
    return user
