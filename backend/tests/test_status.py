import json
from time import sleep
from fastapi.testclient import TestClient
from backend.app.api import app
#from backend.settings import settings
# Отладка
from backend.settings import settings_Dev
from backend.app.MyBox import MyBox, main


def test_box():
    machine = MyBox()
    assert machine.state == 'Введите пароль'
    machine.bad_password()
    assert machine.state == 'Неверный пароль'
    machine.repeat()
    assert machine.state == 'Введите пароль'
    machine.good_password()
    assert machine.state == 'Дверь открыта'
    sleep(machine.TIMEOUT+1)
    assert machine.state == 'Закройте дверь'
    machine.close()
    assert machine.state == 'Введите пароль'


def test_home():
    client = TestClient(app)
    result = client.get('/')
    assert result.status_code == 200
    assert result.json() == {
        "Status": "OK"
    }

def test_state():
    machine = MyBox()
    client = TestClient(app)
    result = client.get('/state')
    assert result.status_code == 200
    assert result.json() == {
        "stateBox": machine.state
    }

def test_open():
    machine = MyBox()
    client = TestClient(app)
    result = client.post('/open', json={'password':'qwerty'})
    machine.good_password()
    assert result.status_code == 200
    assert result.json() == {
        "stateBox": machine.state
    }


def test_close():
    machine = MyBox()
    client = TestClient(app)
    result = client.get('/close')
    assert result.status_code == 200
    assert result.json() == {
        "stateBox": machine.state
    }

def test_repeat():
    machine = MyBox()
    client = TestClient(app)
    result = client.get('/repeat')
    assert result.status_code == 200
    assert result.json() == {
        "stateBox": machine.state
    }