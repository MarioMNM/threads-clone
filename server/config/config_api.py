from pydantic_settings import BaseSettings
from dotenv import dotenv_values

config = dotenv_values(".env")

class Settings(BaseSettings):
    db_name: str = config["DB_NAME"]
    db_url: str = config["DB_URL"]
    jwt_secret_key: str = config["SECRET_KEY"]
    jwt_algorithm: str = config["ALGORITHM"]


settings = Settings()