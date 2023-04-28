import uvicorn
from fastapi import FastAPI

from blog_app import models
from blog_app.database import engine
from blog_app.routers import user, blog, authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app)
