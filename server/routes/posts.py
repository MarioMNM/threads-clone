from typing import List
from fastapi import APIRouter, Body, Depends, Request, status

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
    post: Post = Body(...),
    current_user: User = Depends(get_current_user_from_token),
):
    return posts_rules.create_post(request, post, current_user)


@router.get("/", response_description="List posts", response_model=List[Post])
async def list_posts(request: Request):
    return posts_rules.list_posts(request, 100)


@router.get("/{post_id}", response_description="Post", response_model=Post)
async def find_post(request: Request, post_id: str):
    return posts_rules.find_post(request, post_id)


@router.delete(
    "/{post_id}",
    response_description="Delete a post",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(request: Request, post_id: str):
    return posts_rules.delete_post(request, post_id)


@router.put("/like/{post_id}", status_code=status.HTTP_200_OK)
async def like_unlike_post(
    request: Request,
    post_id: str,
    current_user: User = Depends(get_current_user_from_token),
):
    return posts_rules.like_unlike_post(request, post_id, current_user)


@router.put("/reply/{post_id}", status_code=status.HTTP_200_OK)
async def reply_post(
    request: Request,
    post_id: str,
    current_user: User = Depends(get_current_user_from_token),
    post_text: dict = Body(...),
):
    return posts_rules.reply_post(
        request,
        post_id,
        current_user,
        post_text,
    )
