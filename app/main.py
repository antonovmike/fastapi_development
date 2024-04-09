import psycopg2
import time

from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from typing import List

from . import models
from .database import engine, get_db
from .schemas import PostCreate, PostResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', 
            password='123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        # If I set up wrong password start uvicorn app.main:app --reload
        # see this error, then change passwird to correct one I will still
        # in the loop. Even Ctrl+C doesn't help. But in the video this code
        # works fine: https://youtu.be/0sOvCWFmrtA?feature=shared&t=14803
        time.sleep(2)


# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#     {"title": "Favorite foods", "content": "I like pizza", "id": 2}
# ]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     print("Latest post:", post)

#     return post


@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')

    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    posts_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post
