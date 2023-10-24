import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

db_client = MongoClient(
    f"mongodb+srv://{os.getenv('DB_DEV_USER')}:{os.getenv('DB_DEV_PASSWORD')}@threads-clone.nocwdvz.mongodb.net/?retryWrites=true&w=majority"
).dev
