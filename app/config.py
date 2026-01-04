from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "RSVP Event Management API"
    DEBUG: bool = False
    
    # Database Settings
    # We use Field(validation_alias) to map the .env key to this variable
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    
    # Security (if you add Auth later)
    SECRET_KEY: str = Field("secret", validation_alias="SECRET_KEY")

    # This tells Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single instance to be imported elsewhere
settings = Settings()