from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request, Response, status
from typing import Annotated, List, Optional
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from bson import ObjectId
from typing import Dict
from fastapi.security import OAuth2

from pydantic import BaseModel
from db.models.user import User

import rules.users as users_rules
from config.config_api import settings

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
    

router = APIRouter(prefix="/users", tags=["Users"])

oauth2 = OAuth2PasswordBearerWithCookie(tokenUrl="login")


async def get_current_user(request: Request, token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_rules.get_collection_users(request).find_one(
        {"_id": ObjectId(user_id)}
    )
    if user is None:
        raise credentials_exception
    return User(**user)
    

@router.get("/test")
async def read_items(cookie: Optional[str] = Header(None)):
    return {"Cookie": cookie}


@router.post(
    "/signup",
    response_description="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create_user(request: Request, response: Response, user=Body(...)):
    return users_rules.create_user(request, response, user)


# TODO: refactor LoginRequest
class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    access_token = users_rules.login_user(request, response, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout_user(response: Response):
    users_rules.logout(response)


# TODO: add "/follow/:id" route
@router.post("/follow/{id}", response_model=User)
async def follow_unfollow_user(request: Request, id: str):
    return users_rules.follow_unfollow_user(request, id)


@router.get("/", response_description="List users", response_model=List[User])
async def list_users(request: Request):
    return users_rules.list_users(request, 100)


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user


@router.get(
    "/{id}", response_description="Get a single user by id", response_model=User
)
async def find_user(request: Request, id: str):
    return users_rules.find_user(request, id)


@router.delete(
    "/{id}",
    response_description="Delete a user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(request: Request, id: str):
    return users_rules.delete_user(request, id)

