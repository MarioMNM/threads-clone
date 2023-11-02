from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

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


def find_post(request: Request, post_id: ObjectId):
    if post := get_collection_posts(request).find_one({"_id": post_id}):
        return Post(**post)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} not found!",
    )


def delete_post(request: Request, post_id: ObjectId):
    deleted_post = get_collection_posts(request).delete_one({"_id": post_id})

    if deleted_post.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found!",
        )


def like_unlike_post(
    request: Request,
    post_id: str,
    current_user: User,
):
    post = get_collection_posts(request).find_one({"_id": post_id})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found!",
        )

    user_liked_post = current_user.id in post.get("likes")

    if user_liked_post:
        # Unlike post
        get_collection_posts(request).update_one(
            {"_id": post_id}, {"$pull": {"likes": current_user.id}}
        )
        return {"detail": "Post unliked successfully"}
    else:
        # Like post
        get_collection_posts(request).update_one(
            {"_id": post_id}, {"$push": {"likes": current_user.id}}
        )
        return {"detail": "Post liked successfully"}


def reply_post(
    request: Request,
    post_id: str,
    current_user: User,
    post_text: dict,
):
    if not post_text.get("text"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field is required",
        )

    post = get_collection_posts(request).find_one({"_id": post_id})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found!",
        )

    reply = {
        "userId": current_user.id,
        "text": post_text.get("text"),
        "username": current_user.username,
        "userProfilePic": current_user.profilePic,
    }

    get_collection_posts(request).update_one(
        {"_id": post_id}, {"$push": {"replies": jsonable_encoder(reply)}}
    )

    return reply


def get_feed(request: Request, current_user: User):
    following = current_user.following
    posts = (
        get_collection_posts(request)
        .find({"postedBy": {"$in": following}})
        .sort("updatedAt", -1)
    )

    return list(posts)
