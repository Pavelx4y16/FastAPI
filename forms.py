from typing import Optional

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str = "No description"
    published: bool = False
