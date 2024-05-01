from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, oauth2
from ..schemas import PostCreate, PostResponse
from app.database import get_db

router = APIRouter()


router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


@router.get("/", response_model=List[PostResponse])
async def get_posts(
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10
    ):
    #posts?limit=2
    print(limit)
    posts = db.query(models.Post).limit(limit).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(
        post: PostCreate, db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest", response_model=PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    latest_post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No posts found")

    return latest_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int, db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
        ):
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(
        id: int, post: PostCreate, db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
        ):
    print(current_user)
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts_query.first()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
            )
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    posts_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post
