from fastapi import HTTPException, status

from app.constants.token_constants import TOKEN_HEADERS


class InvalidAuthenticationCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверные учетные данные для аутентификации.",
            headers=TOKEN_HEADERS.get("headers")
        )


class TokenExpired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истек.",
            headers=TOKEN_HEADERS.get("headers")
        )
