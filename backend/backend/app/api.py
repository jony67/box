from fastapi import FastAPI
from backend.app.box_router import router
from fastapi.middleware.cors import CORSMiddleware
from backend.settings import settings_Dev


app = FastAPI(
    title=settings_Dev.APP_NAME,
    version=settings_Dev.VERSION,
    description=settings_Dev.DESCRIPTION
    )


app.add_middleware(
        CORSMiddleware,
        allow_origins=settings_Dev.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.include_router(router)