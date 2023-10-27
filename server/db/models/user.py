from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, SecretStr
from bson import ObjectId


class User(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(unique=True, index=True)
    profilePic: str = ""
    bio: str = ""
    password: SecretStr
    followers: List[str] = []
    following: List[str] = []

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
                "password": "foobar",
                "profilePic": "https://avatars.githubusercontent.com/u/117460164?s=400&u=e32c1ba05557a3f647818d2a767f2f08dee48851&v=4",
                "bio": "Mathematician & Data Scientist. AI enthusiast. Web development passionate.",
                "followers": [],
                "following": [],
            }
        }


class UserData(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(unique=True, index=True)
    profilePic: Optional[str] = ""
    bio: Optional[str] = ""

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Mario",
                "email": "mario@gmail.com",
                "username": "mariomnm",
                "profilePic": "https://avatars.githubusercontent.com/u/117460164?s=400&u=e32c1ba05557a3f647818d2a767f2f08dee48851&v=4",
                "bio": "Mathematician & Data Scientist. AI enthusiast. Web development passionate.",
            }
        }
