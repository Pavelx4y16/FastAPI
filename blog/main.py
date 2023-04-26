import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from forms import Blog
import models
from database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post('/blog')
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blogs')
def blog_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get('/blogs/{id}')
def blog_list(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    return blog


if __name__ == "__main__":
    uvicorn.run(app)
