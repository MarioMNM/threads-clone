from fastapi import APIRouter, Body, Depends, Request, Response, status

import rules.posts as posts_rules
from db.models.post import Post
from db.models.user import User
from routes.users import get_current_user_from_token

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/create",
    response_description="Create a new post",
    status_code=status.HTTP_201_CREATED,
    response_model=Post,
)
async def create_post(
    request: Request,
    response: Response,
    post: Post = Body(...),
    current_user: User = Depends(get_current_user_from_token),
):
    return posts_rules.create_post(request, response, post, current_user)
