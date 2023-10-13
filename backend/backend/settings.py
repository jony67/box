from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, constr
from pydantic_settings import BaseSettings
from pathlib import Path

ENV_DEV_PATH = Path(Path(__file__).parent,'.dev.env')
ENV_PROD_PATH = Path(Path(__file__).parent,'.prod.env')

class User(BaseModel):
    """
        Проверка пароля.
        - обязательное поле,
        - строка,
        - длина от 5 до 10 символов.

        :param password: Пароль.

    """
    password: constr(min_length=5, max_length=10)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "password": "12345",
                }
            ]
        }
    }




class Settings(BaseSettings):
    """
        Базовые настройки приложения
    """
    MY_PASWD: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://127.0.0.1:8000/',
        'http://localhost:8000/'
        ]
    # Необязательные поля
    APP_NAME: Optional[str] = None
    VERSION: Optional[str] = None
    DESCRIPTION: Optional[str] = None


class DevSettings(Settings):
    """
        Настройки среды разработки
    """
    class Config:
        env_file = ENV_DEV_PATH
        env_file_encoding = 'utf-8'   


class ProdSettings(Settings):
    """
        Настройки среды производства
    """
    class Config:
        env_file = ENV_PROD_PATH
        env_file_encoding = 'utf-8'


settings_Dev = DevSettings()
#settings_Prod = ProdSettings()
