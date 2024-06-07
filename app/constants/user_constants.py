USER_API_PREFIX = "/user"

USER_REGISTER_DETAIL = {
    400: "Такого домена электронной почты не существует.",
    406: "Пароли не совпадают.",
    409: "Пользователь с такими данными уже существует.",
    413: "Username должен быть меньше 30 символов.",
}

USER_REGISTER_BAD_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_REGISTER_DETAIL.get(400)}
                    }
            }
    },
    406: {
        "description": "Error: Not Acceptable",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_REGISTER_DETAIL.get(406)}
                    }
            }
    },
    409: {
        "description": "Error: Conflict",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_REGISTER_DETAIL.get(409)}
                    }
            }
    },
    413: {
        "description": "Error: Request Entity Too Large",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_REGISTER_DETAIL.get(413)}
                    }
            }
    }
}


USER_LOGIN_DETAIL = {
    400: "Пользователь не найден.",
    404: "Неверный username/email или пароль."
}

USER_LOGIN_BAD_RESPONSES = {
    400: {
        "description": "Error: Bad Request",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_LOGIN_DETAIL.get(400)}
                    }
            }
    },
    404: {
        "description": "Error: Bad Request",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": USER_LOGIN_DETAIL.get(404)}
                    }
            }
    }
}


SUBSCRIPTION_DETAIL = {
    404: "Подписки на пользователя не существует!",
    406: "Вы не можете подписаться на самого себя!",
    409: "Вы уже подписаны на данного пользователя!",
}

SUBSCRIPTION_BAD_RESPONSES = {
    400: {
        "description": "Error: Bad Request",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": SUBSCRIPTION_DETAIL.get(400)}
                    }
            }
    },
    406: {
        "description": "Error: Not Acceptable",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": SUBSCRIPTION_DETAIL.get(406)}
                    }
            }
    },
    409: {
        "description": "Error: Conflict",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": SUBSCRIPTION_DETAIL.get(409)}
                    }
            }
    },
}


NOTIFICATION_DETAIL = {
    409: "Вы уже установили время для данного пользователя!",
}

NOTIFICATION_BAD_RESPONSES = {
    409: {
        "description": "Error: Conflict",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": NOTIFICATION_DETAIL.get(409)}
                    }
            }
    },
}
