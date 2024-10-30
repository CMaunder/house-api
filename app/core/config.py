import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PROJECT_NAME:str = "HouseAPI"
    PROJECT_VERSION: str = "1.0.0"
    #DATABASE SETTINGS
    MYSQL_USER : str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD : str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER : str = os.getenv("MYSQL_SERVER","localhost")
    DEFAULT_DB : str = os.getenv("DEFAULT_DB","telegraphhouse")
    DATABASE_URL: str = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DEFAULT_DB}"
    #RABBITMQ SETTINGS
    RABBITMQ_USER : str = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD : str = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_SERVER : str = os.getenv("RABBITMQ_SERVER","localhost")

settings = Settings()