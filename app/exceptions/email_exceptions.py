EMAIL_SENDING_ERROR = {
    500: "Ошибка отправки email-сообщения"
}

EMAIL_SENDING_RESPONSES = {
    500: {
        "description": "Error: Server Error",
        "content":
            {
                "application/json":
                    {
                        "example": {"detail": EMAIL_SENDING_ERROR.get(500)}
                    }
            }
    }
}
