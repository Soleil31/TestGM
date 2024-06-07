from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import timedelta


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


class ListUsersSchema(BaseModel):
    users: List["UserBaseSchema"]


class NotificationTimeDeltaSchema(BaseModel):
    notification_timedelta: timedelta = Field(
        ...,
        description="Время до ДР, когда нужно отправить уведомление. Например, '1 day' для уведомления за день до ДР.",
        examples=["1 day", "2 hours", "10 minutes"]
    )
