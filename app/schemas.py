

from datetime import datetime
from psycopg2 import DATETIME
from pydantic import BaseModel, EmailStr, conint
from typing import Optional 


class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode= True    

    
class post(BaseModel):
    title: str
    content: str
    published: bool=True
    owner: UserOut

    class Config:
        orm_mode= True    

class postout(post):
    id: int
    created_at: datetime
    creator_id: int
    class Config:
        orm_mode= True

class Postoutvotes(BaseModel):
    Post: postout
    votes: int
    class Config:
        orm_mode= True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)