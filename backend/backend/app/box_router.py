from fastapi import APIRouter, HTTPException, status
from backend.app.MyBox import MyBox
from backend.settings import User, settings_Dev


router = APIRouter()

# Экземпляр класса камеры хранения:
my_box = MyBox()
#my_box.set_state('Дверь открыта')


@router.get('/')
async def get_status() -> dict:
    return {"Status": "OK"}


@router.get('/state')
async def get_state() -> dict:
    state = my_box.state
    if (state):
        return {"stateBox": state}
    
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
	    detail="Проблемы с бэкендом...",
        )


@router.get('/close')
async def close_box() -> dict:
    state = my_box.state
    if (state):
        if ((state == 'Дверь открыта') or (state == 'Закройте дверь')):
            my_box.close()
            state = my_box.state
            return {"stateBox": state}    
        else:    
            return {"stateBox": state}
    
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
	    detail="Проблемы с бэкендом...",
        )
 

@router.post('/open')
async def open_box(user: User) -> dict:
    state = my_box.state
    if (state):
        if (user.password == settings_Dev.MY_PASWD):
            if (state == 'Введите пароль'): 
                my_box.good_password()
                state = my_box.state           
                answer = {"stateBox": state}
            else:
                answer = {"stateBox": state}
    
        else:
            my_box.bad_password()
            state = my_box.state
            answer = {"stateBox": state}
        return answer
    
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
	    detail="Проблемы с бэкендом...",
        )
    

@router.get('/repeat')
async def repeat_input() -> dict:
    state = my_box.state
    if (state):
        if (state != ('Неверный пароль')):        
            return {"stateBox": state}
        else:
            my_box.repeat()
            state = my_box.state
            return {"stateBox": state}
    raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
	        detail="Проблемы с бэкендом...",
            )  
