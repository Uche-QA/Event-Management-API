from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "RSVP Event Management API"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    
    SECRET_KEY: str
    
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
   
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()