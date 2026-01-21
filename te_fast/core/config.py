from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My API"
    debug: bool = True
    database_url: str = "sqlite:///app.db"
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
