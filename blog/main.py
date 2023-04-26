import uvicorn
from fastapi import FastAPI

from forms import Blog
import models
from database import engine


app = FastAPI()
models.Base.metadata.create_all(engine)

@app.post('/blog')
def create(blog: Blog):
    return {'title': blog.title, 'description': blog.description, 'published': blog.published}


if __name__ == "__main__":
    uvicorn.run(app)
