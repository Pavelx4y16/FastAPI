import uvicorn
from fastapi import FastAPI

from schemas import Blog

app = FastAPI()


@app.post('/blog')
def create(blog: Blog):
    return {'title': blog.title, 'description': blog.description, 'published': blog.published}


if __name__ == "__main__":
    uvicorn.run(app)
