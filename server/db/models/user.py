from typing import Optional
from pydantic import BaseModel, EmailStr, Field, SecretStr
from bson import ObjectId


class User(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(unique=True, index=True)
    profilePic: Optional[str] = ""
    bio: Optional[str] = ""
    password: SecretStr

    class Config:
        populate_by_name = True
        arbitrary_types_allowed=True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Mario",
                "email": "mario@gmail.com",
                "username": "mariomnm",
                "password": "foobar",
                "profilePic": "https://avatars.githubusercontent.com/u/117460164?s=400&u=e32c1ba05557a3f647818d2a767f2f08dee48851&v=4",
                "bio": "Mathematician & Data Scientist. AI enthusiast. Web development passionate."
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
                "bio": "Mathematician & Data Scientist. AI enthusiast. Web development passionate."
            }
        }