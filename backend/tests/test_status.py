from time import sleep
from fastapi.testclient import TestClient
from backend.app.api import app
#from backend.settings import settings
# Отладка
from backend.settings import settings_Dev
from backend.app.MyBox import MyBox

def test_box():
    state = MyBox()
    assert state.state == 'Введите пароль'
    state.bad_password()
    assert state.state == 'Неверный пароль'
    state.repeat()
    assert state.state == 'Введите пароль'
    state.good_password()
    assert state.state == 'Дверь открыта'
    sleep(state.TIMEOUT+1)
    assert state.state == 'Закройте дверь'
    state.close()
    assert state.state == 'Введите пароль'


def test_main():
    client = TestClient(app)
    result = client.get('/')
    assert result.status_code == 200
    assert result.json() == {
        "Status": "OK"
    }

def test_state():
    state = MyBox().state
    client = TestClient(app)
    result = client.get('/state')
    assert result.status_code == 200
    assert result.json() == {
        "stateBox": state
    }