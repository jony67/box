from fastapi import FastAPI
from backend.app.box_router import router
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

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


app.include_router(router)