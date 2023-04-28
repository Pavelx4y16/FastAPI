from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from oauth2 import get_current_user
from repository import blog as blog_utils

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.get('/', response_model=List[schemas.ShowBlog])
def blog_list(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_utils.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def blog_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_utils.get_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_utils.create(request=request, db=db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_utils.destroy(id=id, db=db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_utils.update(id=id, request=request, db=db)
