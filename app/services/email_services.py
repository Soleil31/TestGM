import logging
from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType

from settings.loader import EMAIL_CONFIGURATION
from app.exceptions.email_exceptions import EMAIL_SENDING_ERROR
from database import crud


async def notify_about_birthday() -> None:

    notifications = await crud.read_list_of_notifications_to_send_email()

    if notifications is not None:

        for notification in notifications:

            subscribe = await crud.read_subscribe_by_id(
                subscribe_id=notification.subscription_id
            )

            user_to_notify = await crud.read_user_email_by_user_id(user_id=subscribe.follower_id)

            user_notify_about = await crud.read_user_email_by_user_id(user_id=subscribe.followed_id)

            await send_message_to_email(
                text=f"Скоро у пользователя {user_notify_about.email} День Рождения!",
                subject="Напоминание о Дне Рождения!",
                recipients=[user_to_notify.email],
                subtype=MessageType.plain
            )

            await crud.update_notification_time_by_id(notification_id=notification.id)


async def send_message_to_email(
        text: str,
        subject: str,
        recipients: List[str],
        subtype: MessageType
) -> None:

    try:

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=text,
            subtype=subtype
        )

        fm = FastMail(EMAIL_CONFIGURATION)

        await fm.send_message(message=message)

    except Exception as e:

        logging.error(f"Не удалось отправить сообщение: {e}")
        raise EMAIL_SENDING_ERROR()
