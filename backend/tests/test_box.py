# -*- coding: utf-8 -*-
"""Модуль тестов

@author: sev
"""

import pytest
from time import sleep
from fastapi.testclient import TestClient
from backend.app.api import app
from backend.app.MyBox import MyBox


@pytest.fixture
def my_class():
    return MyBox()


def test_box(my_class):
    # Тест камеры хранения
    assert my_class.state == 'Введите пароль'
    my_class.bad_password()
    assert my_class.state == 'Неверный пароль'
    my_class.repeat()
    assert my_class.state == 'Введите пароль'
    my_class.good_password()
    assert my_class.state == 'Дверь открыта'
    sleep(my_class.TIMEOUT+1)
    assert my_class.state == 'Закройте дверь'
    my_class.close()
    assert my_class.state == 'Введите пароль'
    print(my_class)


# Тест FastAPI
def test_home():
    # Проверка WEB
    client = TestClient(app)
    result = client.get('/')
    assert result.status_code == 200
    assert result.json() == {
        "Status": "OK"
    }


def test_state(my_class):
    # Текущее состояние камеры хранения
    client = TestClient(app)
    result = client.get('/state')
    assert result.status_code == 200
    assert result.json() == {
        "state": my_class.state
    }

def test_open_good(my_class):
    # Открываем камеру хранения
    client = TestClient(app)
    result = client.post('/open', json={'password':'qwerty'})
    my_class.good_password()
    assert result.status_code == 200
    assert result.json() == {
        "state": my_class.state
    }
    # Закрываем камеру хранения
    result = client.get('/close')
    my_class.close()
    assert result.status_code == 200
    assert result.json() == {
        "state": my_class.state
    }

def test_open_bad(my_class):
    # Пароль не правильный
    client = TestClient(app)
    result = client.post('/open', json={'password':'qeqweqweq'})
    my_class.bad_password()
    assert result.status_code == 200
    assert result.json() == {
        "state": my_class.state
    } 

def test_repeat(my_class):
    # Повторить ввод
    client = TestClient(app)
    result = client.get('/repeat')
    assert result.status_code == 200
    assert result.json() == {
        "state": my_class.state
    }