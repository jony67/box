from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.settings import settings

app = FastAPI(
    title="Камера хранения",
    description="Бэкенд, реализующий модель камеры хранения"
    )

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

class Status(BaseModel):
    code: int = 200  
    status: str = "Ok"


@app.get(settings.main_url)
async def get_state() -> dict:
    return dict(Status())