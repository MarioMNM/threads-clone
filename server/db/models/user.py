from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field, SecretStr
from bson import ObjectId

from utils.helpers.datetime_helpers import datetime_now


class User(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(unique=True, index=True)
    profilePic: None | str = ""
    bio: None | str = ""
    password: SecretStr
    followers: None | List[str] = []
    following: None | List[str] = []
    updatedAt: datetime = Field(default_factory=datetime_now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }
        json_schema_extra = {
            "example": {
                "name": "Mario",
                "email": "mario@gmail.com",
                "username": "mariomnm",
                "password": "foobar"
            }
        }
