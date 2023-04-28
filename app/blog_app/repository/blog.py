from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog_app import models
from blog_app import schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()

    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def destroy(id: int, db: Session):
    items = db.query(models.Blog).filter(models.Blog.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()

    return 'updated'


def get_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    return blog
