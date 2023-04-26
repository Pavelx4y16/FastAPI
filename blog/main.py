import uvicorn
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from forms import Blog
import models
from database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return 'done'


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    blog.update({models.Blog.title: request.title, models.Blog.body: request.body})
    db.commit()

    return 'updated'


@app.get('/blogs')
def blog_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get('/blogs/{id}', status_code=200)
def blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found.")
    return blog


if __name__ == "__main__":
    uvicorn.run(app)
