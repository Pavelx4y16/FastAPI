from typing import List

import models
import schemas
from database import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.get('/', response_model=List[schemas.ShowBlog])
def blog_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    items = db.query(models.Blog).filter(models.Blog.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()

    return 'updated'


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    return blog
