from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "Favorite foods", "content": "I like pizza", "id": 2}
]

@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.model_dump()) # dict() is deprecated
    return {"new_post": f"title: {post.title} content: {post.content}"}

