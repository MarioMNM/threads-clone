from fastapi import Request, Response

from db.models.post import Post
from db.models.user import User


def get_collection_posts(request: Request):
    return request.app.database["posts"]


def create_post(
    request: Request,
    response: Response,
    post: Post,
    current_user: User,
):
    maxLength = 500
    if post.length > maxLength:
        return 
    

