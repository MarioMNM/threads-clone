from typing import Annotated, List

import rules.users as users_rules
from db.models.user import User
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from utils.helpers.auth import OAuth2PasswordBearerWithCookie

router = APIRouter(prefix="/users", tags=["Users"])

oauth2 = OAuth2PasswordBearerWithCookie(tokenUrl="login")


async def get_current_user_from_token(request: Request, token: str = Depends(oauth2)):
    return users_rules.get_current_user_from_token(request, token)


@router.post(
    "/signup",
    response_description="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create_user(request: Request, response: Response, user: User = Body(...)):
    return users_rules.create_user(request, response, user)


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    access_token = users_rules.login_user(request, response, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    users_rules.logout(response)


@router.post("/follow/{id}", status_code=status.HTTP_200_OK)
async def follow_unfollow_user(
    request: Request, id: str, current_user: User = Depends(get_current_user_from_token)
):
    return users_rules.follow_unfollow_user(request, id, current_user)


@router.get("/", response_description="List users", response_model=List[User])
async def list_users(request: Request):
    return users_rules.list_users(request, 100)


@router.get("/me")
async def current_user(user: User = Depends(get_current_user_from_token)):
    return user


@router.get(
    "/profile/{query}",
    response_description="Get a single user by id",
    response_model=User,
)
async def find_user(request: Request, query: str):
    return users_rules.find_user(request, query)


@router.delete(
    "/{id}",
    response_description="Delete a user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(request: Request, id: str):
    return users_rules.delete_user(request, id)
