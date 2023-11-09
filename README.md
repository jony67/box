# Модель системы автоматической камеры хранения (бэкенд: Python, FastAPI, тесты Pytest; фронтенд: React)
## Оглавление
1. [Используемые технологии и компоненты](#Используемые-технологии-и-компоненты)
2. [Описание](#Описание)
3. [Тесты (Pytest)](#Тесты-(Pytest))
3. [Состав проекта](#Состав-проекта)
4. [Установка и запуск в локальной среде](#Установка-и-запуск-в-локальной-среде)
## Используемые технологии и компоненты
Модель камеры хранения реализована по клиент-серверной схеме бэкенд + фронтенд, взаимодействующих между собой через API.
### - Бэкенд:
Бэкенд представляет собой консольное приложение, написанное на языке Python. Бизнес-логика камеры хранения реализована с использованием библиотеки конечного автомата [transitions](https://github.com/pytransitions/transitions). 
После ввода правильного пароля система переходит в состояние «Дверь открыта» и запускается таймер, по истечении времени которого система переходит в состояние «Закройте дверь». Состояние открытой двери моделируется в отдельном потоке, который «хранит» информацию об открытой двери и мониторит факт закрытия двери. После получения сигнала закрытия двери поток разрушается.
API реализован с использованием фреймворка FastAPI.
[![API (Swagger UI)](/_jpg/2.jpg)]
### - Фронтенд:
Фронтенд представляет собой web приложение, реализованное с использованием JavaScript библиотеки React и выполняет функцию графического интерфейса системы.
|[![React-1](/_jpg/3.jpg)][![React-2](/_jpg/4.jpg)]|
|[![React-3](/_jpg/5.jpg)][![React-4](/_jpg/6.jpg)]|
|[![React-5](/_jpg/7.jpg)][![React-6](/_jpg/8.jpg)]|

[:arrow_up:Оглавление](#Оглавление)

## Описание
Камера хранения представляет собой шкаф с дверцей, оснащенной электрическим замком. Также камера хранения имеет графический интерфейс, позволяющий ввести пароль. При совпадении пароля с сохраненным в системе дверь камеры хранения автоматически открывается. При закрытии двери замок закрывается, и система переходит в исходное состояние – ожидание ввода пароля. Если дверь не будет закрыта в течение заданного промежутка времени, в графическом интерфейсе должно быть выведено предупреждение. После закрытия двери предупреждение отключается, система переходит в исходное состояние.
[![Модель](/_jpg/1.jpg)]

[:arrow_up:Оглавление](#Оглавление)

## Тесты (Pytest)
Бэкенд покрыт тестами на 100%__
[![Покрытие тестами](/_jpg/9.jpg)]

[:arrow_up:Оглавление](#Оглавление)

## Состав проекта
В папке **backend/backend/** находятся:
1. `./main.py` – точка входа бэкенда.
2. `./settings.py` – файл базовых настроек приложения и переменных окружения для среды разработки и производства.
3. Файлы модели камеры хранения (./app/):
- `MyBox.py` – модель;
- `diagram.py` – модуль построения диаграммы состояний;
- `scenario.py` – сценарий работы модели в 2-потоках (имитация работы бэкенда в многопользовательском режиме);
- `api.py`, `box_router.py` – модули FastAPI.
В папке **backend/tests/** находятся тесты.
В папке **frontend/** находятся файлы фронтенда (React).
В составе проекта отсутствуют файлы переменных окружения (*.dev.env* и *.prod.env*), которые нужно создать самостоятельно:
- `APP_NAME` = Камера хранения
- `VERSION` = 0.1.0
- `DESCRIPTION` = Бэкенд, реализующий модель камеры хранения
- `MY_PASWD` = qwerty

[:arrow_up:Оглавление](#Оглавление)

## Установка и запуск в локальной среде
Открыть терминал и выполнить:
```
	$ git clone https://github.com/jony67/box
	$ cd box/backend
	$ poetry install
	$ .venv/Scripts/activate
	$ python backend/main.py
```
Открыть новый терминал, перейти в каталог box/backend и выполнить:
```
	$ poetry run curl http://127.0.0.1:8000/
```
Результат:
`{"Status":"OK"}`__
Бэкенд запущен.
```
	$ yarn install
	$ yarn dev
```
Запустить веб-браузер, набрать в адресной строке:
http://127.0.0.1:3000/

[:arrow_up:Оглавление](#Оглавление)