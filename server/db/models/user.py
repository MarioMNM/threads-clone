from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from utils.helpers.datetime_helpers import datetime_now


class User(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(..., unique=True, index=True)
    email: EmailStr = Field(..., unique=True, index=True)
    profilePic: None | str = ""
    bio: None | str = ""
    password: str
    followers: None | List[str] = []
    following: None | List[str] = []
    updatedAt: datetime = Field(default_factory=datetime_now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Mario",
                "email": "mario@gmail.com",
                "username": "mariomnm",
                "password": "foobar",
            }
        }
