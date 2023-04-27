from typing import List

import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from hashing import Hash
from database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["users"])
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    items = db.query(models.Blog).filter(models.Blog.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def destroy(id: int, db: Session = Depends(get_db)):
    items = db.query(models.User).filter(models.User.id == id)

    if not items.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with the id {id} is not found.")

    items.delete(synchronize_session=False)
    db.commit()

    return 'done'


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()

    return 'updated'


@app.put('/users/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["users"])
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


@app.get('/blogs', response_model=List[schemas.ShowBlog], tags=["blogs"])
def blog_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get('/users', response_model=List[schemas.ShowUser], tags=["users"])
def user_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    return blog


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found.")
    return user


if __name__ == "__main__":
    uvicorn.run(app)
