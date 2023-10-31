from fastapi import APIRouter

import rules.posts as posts_rules
from db.models.post import Post


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
async def test():
    return {"message": "This is a test."}