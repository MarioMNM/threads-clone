from fastapi import Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db.models.user import User
from bson import ObjectId

from utils.helpers.jwt_cookies import create_jwt_set_cookies


crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return crypt.verify(plain_password, hashed_password)


def get_password_hash(password):
    return crypt.hash(password)


def get_collection_users(request: Request):
    return request.app.database["users"]


def find_user(request: Request, id: ObjectId):
    if user := get_collection_users(request).find_one({"_id": id}):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!"
    )


def create_user(request: Request, response: Response, user: User = Body(...)):
    user = jsonable_encoder(user)

    existing_user_email = get_collection_users(request).find_one(
        {"email": user["email"]}
    )
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already in use",
        )

    existing_user_username = get_collection_users(request).find_one(
        {"username": user["username"]}
    )
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use",
        )

    user["password"] = get_password_hash(user["password"])

    new_user = get_collection_users(request).insert_one(user)

    if new_user:
        create_jwt_set_cookies(str(new_user.inserted_id), response)
        created_user = get_collection_users(request).find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data."
    )


def login_user(request: Request, response: Response, user: OAuth2PasswordRequestForm):
    existing_user = User(
        **get_collection_users(request).find_one({"username": user.username})
    )
    existing_user = jsonable_encoder(existing_user)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found"
        )

    correct_pswd = verify_password(user.password, existing_user["password"])
    if not existing_user or not correct_pswd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    encoded_jwt = create_jwt_set_cookies(str(existing_user["_id"]), response)

    return encoded_jwt


def logout(response: Response):
    response.delete_cookie("access_token")


def follow_unfollow_user(request: Request, id: str):
    print(ObjectId(id))
    userToModify = get_collection_users(request).find_one({"_id": ObjectId(id)})
    return userToModify


def list_users(request: Request, limit: int):
    users = list(get_collection_users(request).find(limit=limit))
    return users


def delete_user(request: Request, id: ObjectId):
    deleted_user = get_collection_users(request).delete_one({"_id": id})

    if deleted_user.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!",
        )
