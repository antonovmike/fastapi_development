import psycopg2
import time

from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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
        # wirks fine: https://youtu.be/0sOvCWFmrtA?feature=shared&t=14803
        time.sleep(2)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "Favorite foods", "content": "I like pizza", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # The method "dict" in class "BaseModel" is deprecated
    new_post = models.Post(**post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    print("Latest post:", post)

    return {"latest_detail": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')

    return {"post_detail": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}
