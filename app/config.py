# Configuration & API keys

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    API_KEY: str = "GUVI_SECRET_2026"
    GEMINI_API_KEY: str = "your-gemini-api-key"
    
    # Application
    APP_NAME: str = "Agentic Honey-Pot"
    MOCK_MODE: bool = False
    DEBUG: bool = False
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()