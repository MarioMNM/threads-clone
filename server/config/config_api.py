from pydantic_settings import BaseSettings
from dotenv import dotenv_values

config = dotenv_values(".server.env")

class Settings(BaseSettings):
    db_name: str = config["DB_NAME"]
    db_url: str = config["DB_URL"]
    jwt_secret_key: str = config["SECRET_KEY"]
    jwt_algorithm: str = config["ALGORITHM"]
    db_docker_username: str = config["MONGODB_DOCKER_USERNAME"]
    db_docker_password: str = config["MONGODB_DOCKER_PASSWORD"]
    db_docker_authsource: str = config["MONGODB_DOCKER_AUTHSOURCE"]
    mongodb_server: str = config["MONGODB_SERVER"]


settings = Settings()