from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str = "Empty"


class ShowBlog(Blog):
    class Config:
        orm_mode = True
