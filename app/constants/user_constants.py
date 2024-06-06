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
