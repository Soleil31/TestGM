from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.api.v1.user_router import router as user_router
from database import crud
from app.services.email_services import notify_about_birthday


app = FastAPI(
    debug=True,
    title="Документация API для тестового задания.",
    version="0.0.1",
    docs_url="/",
    root_path="/api/v1",
    description="Докуменатция составлена в рамках задания. Для связи: pozitif0898@gmail.com, +79814063284"
)
app.include_router(router=user_router)
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

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()
scheduler.add_job(crud.delete_expired_tokens, 'interval', hours=12)
scheduler.add_job(notify_about_birthday, 'interval', seconds=15)
scheduler.start()
