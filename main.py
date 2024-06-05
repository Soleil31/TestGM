from fastapi import FastAPI
import logging


app = FastAPI(
    debug=True,
    title="Документация API для тестового задания.",
    version="0.0.1",
    openapi_url="/"
)

logging.basicConfig(level=logging.INFO)
