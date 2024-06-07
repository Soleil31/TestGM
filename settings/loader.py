import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig


load_dotenv()

PG_CONNECTION_URL = os.getenv('PG_CONNECTION_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

EMAIL_CONFIGURATION = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=bool(os.getenv('MAIL_SSL_TLS')),
    USE_CREDENTIALS=bool(os.getenv('USE_CREDENTIALS')),
    VALIDATE_CERTS=bool(os.getenv('VALIDATE_CERTS'))
)
