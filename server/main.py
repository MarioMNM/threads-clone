from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import uvicorn

from routes.api import router as api_router
from config.config_api import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_docker_client = MongoClient(
        host="mongodb",
        port=27017,
        username=settings.db_docker_username,
        password=settings.db_docker_password,
        authSource=settings.db_docker_authsource,
    )
    if not settings.mongodb_server or settings.mongodb_server == "docker":
        mongo_client = mongo_docker_client
    elif settings.mongodb_server == "online":
        mongo_client = MongoClient(settings.db_url)
    else:
        print("Wrong mongodb server provided. Starting on docker server.")
        mongo_client = mongo_docker_client

    app.mongodb_client = mongo_client
    app.database = app.mongodb_client[settings.db_name]
    yield
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":  # this indicates that this a script to be run
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
