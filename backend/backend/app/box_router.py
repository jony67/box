from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.MyBox import MyBox
#from backend.settings import settings
# Отладка
from backend.settings_dev import settings


router = APIRouter()

# Экземпляр класса камеры хранения:
my_box = MyBox()
#my_box.set_state('Дверь открыта')


@router.get(settings.status)
async def get_state() -> dict:
    return {"Status": "OK"}

@router.get(settings.state)
async def get_state() -> dict:
    state = my_box.state
    return {"stateBox": state}

@router.get(settings.close)
async def close_box() -> dict:
    state = my_box.state
    if (state != ('Дверь открыта' or 'Закройте дверь')):        
        return {"stateBox": state}
    else:
        my_box.closed()
        state = my_box.state
        return {"stateBox": state}
    
    
@router.post(settings.open)
async def open_box(name: str) -> dict:
    return {"stateBox": "Good"}   
