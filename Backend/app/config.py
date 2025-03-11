from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """
    Application configuration using pydantic_settings.
    Loads environment variables from a .env file.
    """
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT_ID: str
    AZURE_ENDPOINT: str
    AZURE_OPENAI_VERSION: str
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)