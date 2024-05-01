from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, oauth2
from ..schemas import PostCreate, PostResponse
from app.database import get_db

router = APIRouter()


router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


# @router.get("/", response_model=List[PostResponse])
@router.get("/")
async def get_posts(
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ""
    ):
    # This query returns simply a list of Post objects
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Left and Right Join examples:
    # left_inner_join = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id)
    # print("Left inner join:\n", left_inner_join)
    # left_outer_join = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    # print("Left outer join:\n", left_outer_join)
    # left_inner_join_count = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id)
    # print("Left inner join + count:\n", left_inner_join_count)

    # This query includes complex data types that require special processing
    # In SQLAlchemy 2.0, where the dict(obj) method no longer returns a dictionary for objects as it did in previous versions
    # One solution to this problem, is to replace the line in FastAPI's venv/lib/python3.12/site-packages/fastapi/encoders.py  
    # file where an attempt is made to convert an object to a dictionary. 
    # Replace this line data = dict(obj) with data = dict(obj._asdict()). 
    # It will allow SQLAlchemy 2.0 query results to be processed correctly
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return results


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
