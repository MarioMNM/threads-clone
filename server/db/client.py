import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

db_client = MongoClient(
    os.getenv("DB_URL")
).dev
