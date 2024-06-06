from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBaseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    followers: List[Optional["UserBaseSchema"]]
    following: List[Optional["UserBaseSchema"]]
