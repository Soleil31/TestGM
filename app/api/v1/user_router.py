from fastapi import APIRouter, Response, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import EmailStr
from email_validator import validate_email
from datetime import date

from app.constants.user_constants import USER_API_PREFIX
from app.exceptions.user_exceptions import PasswordsDoNotMatch, TooLongUsername, InvalidEmailDomain, UserExistError
from app.core.security import get_password_hash, verify_password, get_current_user
from app.services.user_services import create_tokens
from app.schemas.token_schemas import AccessTokenSchema
from app.schemas.response_schemas import SuccessResponseSchema
from app.schemas.user_schemas import UserSchema
from app.constants.user_constants import USER_REGISTER_BAD_RESPONSES, USER_LOGIN_BAD_RESPONSES
from database.crud import create_user, read_user_by_username, read_user_by_user_id


router = APIRouter(prefix=USER_API_PREFIX)


@router.post(
    "/register",
    response_model=AccessTokenSchema,
    responses=USER_REGISTER_BAD_RESPONSES,
    tags=["User"]
)
async def register(
        response: Response,
        username: Annotated[str, Form(..., description="Username пользователя. Пример: 'test_username'")],
        email: Annotated[EmailStr, Form(..., description="Email пользователя. Пример: 'temp_mail@temp.com'")],
        password: Annotated[str, Form(..., description="Пароль. Пример: 'qwerty'")],
        password_confirmation: Annotated[str, Form(..., description="Подтверждение пароля. Пример: 'qwerty'")],
        birthday: Annotated[date, Form(..., description="День рождения пользователя. Пример: '2024-01-01'")],
) -> AccessTokenSchema:

    if password != password_confirmation:
        raise PasswordsDoNotMatch()

    if len(username) > 30:
        raise TooLongUsername()

    try:
        validate_email(email)
    except Exception:
        raise InvalidEmailDomain()

    hashed_password = await get_password_hash(password)
    db_user = await create_user(
        username=username,
        email=email,
        hashed_password=hashed_password,
        birthday=birthday
    )

    access_token, refresh_token = await create_tokens(user_id=db_user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none"
    )

    return AccessTokenSchema(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/login",
    response_model=AccessTokenSchema,
    responses=USER_LOGIN_BAD_RESPONSES,
    tags=["User"]
)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> AccessTokenSchema:

    db_user = await read_user_by_username(username=form_data.username)

    result_of_verifying_pass = await verify_password(form_data.password, db_user.hashed_password)

    if not result_of_verifying_pass:
        raise UserExistError()

    access_token, refresh_token = await create_tokens(user_id=db_user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none"
    )

    return AccessTokenSchema(
        access_token=access_token,
        token_type="bearer"
    )


@router.delete(
    "/logout",
    response_model=SuccessResponseSchema,
    tags=["User"]
)
async def logout(
        response: Response,
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> SuccessResponseSchema:

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="none"
    )

    return SuccessResponseSchema(detail="Успешный выход!")


@router.get(
    "/me",
    response_model=UserSchema,
    tags=["User"]
)
async def read_user_me(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserSchema:

    return current_user
