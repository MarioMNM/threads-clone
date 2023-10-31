from datetime import datetime
from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field

from utils.helpers.datetime_helpers import datetime_now


class Post(BaseModel):
    id: ObjectId | str = Field(default_factory=ObjectId, alias="_id")
    postedBy: ObjectId | str
    text: str = Field(..., max_length=500)
    img: str | None
    likes: None | List[ObjectId | str] = []
    replies: List[dict] = []
    updatedAt: datetime = Field(default_factory=datetime_now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "id": "33413dbb2c2ebd225f349ca0",
                "postedBy": "65413dbb2c2ebdf25f349ca0",
                "text": "This is a post.",
            }
        }
