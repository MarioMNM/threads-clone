from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from db.models.post import Post
from db.models.user import User


def get_collection_posts(request: Request):
    return request.app.database["posts"]


def create_post(
    request: Request,
    post: Post,
    current_user: User,
):
    post = jsonable_encoder(post)

    maxLength = 500
    if len(post.get("text")) > maxLength:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Text must be less than ${maxLength} characters",
        )

    post["postedBy"] = current_user.id

    inserted_post = get_collection_posts(request).insert_one(post)
    new_post = get_collection_posts(request).find_one(
        {"_id": inserted_post.inserted_id}
    )
    if new_post:
        return Post(**new_post)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post data."
    )


def list_posts(request: Request, limit: int):
    posts = list(get_collection_posts(request).find(limit=limit))
    return posts
