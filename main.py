from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome"}


# from fastapi.params import Body
# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']} content: {payload['body']}"}


@app.get("/posts")
async def get_posts():
    return {"data": "This is your posts"}


@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.model_dump()) # dict() is deprecated
    return {"new_post": f"title: {post.title} content: {post.content}"}

# https://youtu.be/0sOvCWFmrtA?feature=shared&t=5335