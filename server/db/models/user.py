from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from utils.helpers.datetime_helpers import datetime_now


class UserData(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(..., unique=True, index=True)
    email: EmailStr = Field(..., unique=True, index=True)
    profilePic: None | str = ""
    bio: None | str = ""

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Mario",
                "email": "mario@gmail.com",
                "username": "mariomnm",
            }
        }


class User(UserData):
    password: str
    followers: None | List[str] = []
    following: None | List[str] = []
    updatedAt: datetime = Field(default_factory=datetime_now)


class UpdateUser(UserData):
    password: None | str
    updatedAt: datetime = Field(default_factory=datetime_now)
