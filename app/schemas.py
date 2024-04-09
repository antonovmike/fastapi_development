from datetime import datetime
from pydantic import BaseModel, EmailStr


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


# email_validator has being install: fastapi[all] 
# otherwise it can be installed: pip install email-validator
# because we need EmailStr
class UserCreate(BaseModel):
    email: EmailStr 
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # class Config:
    #     orm_mode = True
