from fastapi import HTTPException, status

from app.constants.user_constants import (
    USER_REGISTER_DETAIL, USER_LOGIN_DETAIL,
    SUBSCRIPTION_DETAIL, NOTIFICATION_DETAIL
)


class PasswordsDoNotMatch(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=USER_REGISTER_DETAIL.get(406)
        )


class TooLongUsername(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=USER_REGISTER_DETAIL.get(413)
        )


class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=USER_REGISTER_DETAIL.get(409)
        )


class InvalidEmailDomain(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_REGISTER_DETAIL.get(400)
        )


class UnmatchedPassOrUsername(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_LOGIN_DETAIL.get(404)
        )


class UserExistError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_LOGIN_DETAIL.get(400)
        )


class SubscriptionAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=SUBSCRIPTION_DETAIL.get(409)
        )


class SubscriptionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=SUBSCRIPTION_DETAIL.get(406)
        )


class SubscriptionDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SUBSCRIPTION_DETAIL.get(404)
        )


class NotificationTimeTooLarge(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NOTIFICATION_DETAIL.get(400)
        )
