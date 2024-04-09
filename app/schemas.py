from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    # Looks like Config is no longer needed in the current version
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    # class Config:
    #     orm_mode = True
