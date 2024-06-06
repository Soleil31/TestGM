from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.user_router import router as user_router


app = FastAPI(
    debug=True,
    title="Документация API для тестового задания.",
    version="0.0.1",
    docs_url="/",
    root_path="/api/v1",
    description="Докуменатция составлена в рамках задания. Для связи: pozitif0898@gmail.com, +79814063284"
)

app.include_router(router=user_router)

logging.basicConfig(level=logging.INFO)

origins = [
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
