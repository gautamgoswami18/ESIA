from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


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
    LLM_PROVIDER: str = "gemini"
    # Groq
    GROQ_API_KEY: str = "GROQ_API_KEY"

    GROQ_MODEL: str ="llama-3.3-70b-versatile"
    # Gemini
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    
    # Ollama
    OLLAMA_MODEL: str = "llama3.2:3b"

    #OLLAMA_BASE_URL=http://localhost:11434
    
    LANGCHAIN_TRACING_V2: bool = False

    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"

    LANGCHAIN_API_KEY: str = "LANGCHAIN_API_KEY"

    LANGCHAIN_PROJECT: str = "ESIA"

    RAG_PROVIDER: str = "langchain"
    
    model_config = SettingsConfigDict(
            env_file=BASE_DIR / ".env",
            extra="ignore"
        )    
settings = Settings()
   
   