from fastapi import APIRouter, Response, Form, Depends, Path, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import EmailStr
from email_validator import validate_email
from datetime import date, timedelta

from app.constants.user_constants import USER_API_PREFIX
from app.exceptions.user_exceptions import (
    PasswordsDoNotMatch, TooLongUsername, InvalidEmailDomain,
    UserExistError, SubscriptionError, NotificationTimeTooLarge
)
from app.core.security import get_password_hash, verify_password, get_current_user
from app.services.user_services import create_tokens
from app.schemas.token_schemas import AccessTokenSchema
from app.schemas.response_schemas import SuccessResponseSchema
from app.schemas.user_schemas import (
    UserSchema, ListUsersSchema, NotificationTimeDeltaSchema,
    UserNotificationsSchema
)
from app.constants.user_constants import (
    USER_REGISTER_BAD_RESPONSES, USER_LOGIN_BAD_RESPONSES, SUBSCRIPTION_BAD_RESPONSES
)
from database import crud


router = APIRouter(prefix=USER_API_PREFIX)


@router.post(
    "/register",
    response_model=AccessTokenSchema,
    responses=USER_REGISTER_BAD_RESPONSES,
    tags=["User"],
    description="Регистрация пользователя."
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
    db_user = await crud.create_user(
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
    tags=["User"],
    description="Логин пользователя."
)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> AccessTokenSchema:

    db_user = await crud.read_user_by_username(username=form_data.username)

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
    tags=["User"],
    description="Выход из аккаунта (удаляем рефреш из куки)."
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
    tags=["User"],
    description="Получение информации о текущем пользователе."
)
async def read_user_me(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserSchema:

    return current_user


@router.get(
    "/list-of-users",
    response_model=ListUsersSchema,
    tags=["User"],
    description="Получение списка всех пользователей."
)
async def read_list_of_users(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> ListUsersSchema:

    users = await crud.read_list_of_users()

    return users


@router.post(
    "/follow-user/{following_user_id}",
    response_model=SuccessResponseSchema,
    responses=SUBSCRIPTION_BAD_RESPONSES,
    tags=["User"],
    description="Подписка на пользователя для уведомления о его Дне Рождения."
)
async def follow_user(
        following_user_id: Annotated[int, Path(title="ID user'а, на которого будет подписка.")],
        notification_timedelta: Annotated[NotificationTimeDeltaSchema, Body(...)],
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> SuccessResponseSchema:

    notification_time = notification_timedelta.notification_timedelta

    if (notification_time.hour > 3 or
        (notification_time.hour == 3 and (notification_time.minute > 0 or notification_time.second > 0))):
        raise NotificationTimeTooLarge()

    if following_user_id == current_user.id:
        raise SubscriptionError()

    subscribe = await crud.create_follow_user(
        current_user_id=current_user.id,
        following_user_id=following_user_id
    )

    notification_timedelta = timedelta(
        hours=notification_time.hour,
        minutes=notification_time.minute,
        seconds=notification_time.second
    )

    await crud.create_notification(
        subscription_id=subscribe.id,
        following_user_id=following_user_id,
        notification_timedelta=notification_timedelta
    )

    return SuccessResponseSchema(
        detail=f"Теперь вы подписаны на пользователя для уведомления о его Дне Рождения!"
    )


@router.delete(
    "/unfollow-user/{following_user_id}",
    response_model=SuccessResponseSchema,
    tags=["User"],
    description="Отписка от пользователя."
)
async def unfollow_user(
        following_user_id: Annotated[int, Path(title="ID user'а, на которого будет подписка.")],
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> SuccessResponseSchema:

    await crud.delete_follow_user(
        current_user_id=current_user.id,
        following_user_id=following_user_id
    )

    return SuccessResponseSchema(
        detail="Теперь вы НЕ подписаны на пользователя для уведомления о его Дне Рождения!"
    )


@router.get(
    "/list-of-notifications",
    response_model=UserNotificationsSchema,
    tags=["User"],
    description="Получение списка всех будущих уведомлений о Днях Рождений."
)
async def get_list_of_notifications(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserNotificationsSchema:

    notifications = await crud.read_list_of_notifications(
        user_id=current_user.id
    )

    return notifications
