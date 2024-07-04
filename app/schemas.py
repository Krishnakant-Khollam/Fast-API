from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_model = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: User

    class Config:
        orm_model = True


class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_model = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
