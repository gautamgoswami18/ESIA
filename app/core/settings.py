from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_SCHEMA: str

    LOG_LEVEL: str
    GOOGLE_API_KEY: str    
    class Config:
        env_file = ".env"
    
settings = Settings()
   
   