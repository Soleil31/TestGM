from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
