from fastapi import APIRouter
from pydantic import BaseModel
#from backend.settings import settings
# Отладка
from backend.settings_dev import settings


router = APIRouter()

class Status(BaseModel):
    """
        Класс для проверки URL
    """
    status: str = "Ok"

@router.get(settings.main_url)
async def get_state() -> dict:
    return dict(Status())