from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr 
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # class Config:
    #     from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # Looks like Config is no longer needed in the current version
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None # It was typo ID is an Integer not String


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore


class VoteResponse(BaseModel):
    message: str
    owner: UserOut

    # class Config:
    #     from_attributes = True