# -*- coding: utf-8 -*-
"""Модуль маршрутизации для FastAPI

@author: sev
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.MyBox import MyBox
from backend.settings import User, settings_Dev


router = APIRouter()

# Экземпляр класса камеры хранения:
my_box = MyBox()


@router.get('/')
async def web_status() -> dict:
    return {"Status": "OK"}


@router.get('/state')
async def get_state_box() -> dict:
    return {"state": my_box.state}


@router.get('/close')
async def close_box() -> dict:
    state = my_box.state
    if ((state == 'Дверь открыта') or (state == 'Закройте дверь')):
        my_box.close()
        state = my_box.state 
    return {"state": state}
 

@router.post('/open')
async def open_box(user: User) -> dict:
    state = my_box.state
    if (user.password == settings_Dev.MY_PASWD):
        if (state == 'Введите пароль'): 
            my_box.good_password()       
            state = {"state": my_box.state}
    else:
        if (my_box.state == 'Введите пароль'):
            my_box.bad_password()
            state = {"state": my_box.state} 
    return state
                

@router.get('/repeat')
async def repeat_input() -> dict:
    state = my_box.state
    if (state == 'Неверный пароль'):
        my_box.repeat()
        state = my_box.state
        state = {"state": my_box.state}
    return state