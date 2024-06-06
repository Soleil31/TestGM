from pydantic import BaseModel


class SuccessResponseSchema(BaseModel):
    detail: str = "Успешно!"
