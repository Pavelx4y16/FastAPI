import uvicorn
from fastapi import FastAPI

import models
from database import engine
from routers import user, blog

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app)
