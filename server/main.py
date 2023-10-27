from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import uvicorn

from routes.api import router as api_router
from config.config_api import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(settings.db_url)
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
