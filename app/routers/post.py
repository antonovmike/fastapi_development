from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

from .. import models, oauth2
from ..schemas import PostCreate, PostResponse
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(
        post: PostCreate, db: Session = Depends(get_db), 
        user_id: int = Depends(oauth2.get_current_user)
    ):
    print(user_id)
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest", response_model=PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No posts found")

    return latest_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts_query.first()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
            )

    posts_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post
