from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    database_name: str = "uhsafclassifier"
    database: str = "mongodb://localhost:27017"


settings = Settings()
