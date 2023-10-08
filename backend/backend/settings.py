from pathlib import Path
from pydantic_settings import BaseSettings
import os
main_url = os.getenv("MAIN_URL")
 
class Settings(BaseSettings):
    """
        Класс настроек
    """
    main_url: str
        

settings = Settings()
