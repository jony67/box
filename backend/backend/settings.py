from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(Path(__file__).parent,'.env')
 
class Settings(BaseSettings):
    main_url: str =""

    model_config = SettingsConfigDict(env_file=ENV_PATH,  env_file_encoding='utf-8')
         

settings = Settings()
#print(Settings().model_dump())