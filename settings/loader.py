import os
from dotenv import load_dotenv


load_dotenv()

PG_CONNECTION_URL = os.getenv('PG_CONNECTION_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
