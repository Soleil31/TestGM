from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import time, datetime


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
    notification_timedelta: time = Field(
        ...,
        description="Время до ДР, когда нужно отправить уведомление. "
                    "Например, '00:30:00' для уведомления за 30 мин до ДР.",
        example="00:30:00"
    )


class UserNotificationsSchema(BaseModel):
    notifications: List["UserNotificationSchema"]


class UserNotificationSchema(BaseModel):
    notification_time: datetime
    user: "UserBaseSchema"
