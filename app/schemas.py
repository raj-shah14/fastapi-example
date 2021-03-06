from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database import Base

class UserCreate(BaseModel):
    email: EmailStr
    password : str
    first_name: str
    last_name: str
    phone_number: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:PostResponse
    Votes:int

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int