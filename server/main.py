from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values

import uvicorn
from routes.api import router as api_router


config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config["DB_URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    yield
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

if __name__ == '__main__': #this indicates that this a script to be run
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)