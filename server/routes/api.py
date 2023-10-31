from fastapi import APIRouter
from routes import users, posts

router = APIRouter(prefix="/api")

router.include_router(users.router)
router.include_router(posts.router)
