from bson import ObjectId
from config.config_api import settings
from db.models.user import User, UserData
from fastapi import Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from utils.helpers.jwt_cookies import create_jwt_set_cookies

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return crypt.verify(plain_password, hashed_password)


def get_password_hash(password):
    return crypt.hash(password)


def get_collection_users(request: Request):
    return request.app.database["users"]


def get_current_user_from_token(request: Request, token: str):
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
    user = get_collection_users(request).find_one({"_id": user_id})
    if user is None:
        raise credentials_exception
    return User(**user)


def find_user(request: Request, query: str | ObjectId):
    if ObjectId.is_valid(query):
        if user := get_collection_users(request).find_one({"_id": query}):
            return UserData(**user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {query} not found!",
        )

    else:
        if user := get_collection_users(request).find_one({"username": query}):
            return UserData(**user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {query} not found!",
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
        return UserData(**created_user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data."
    )


def login_user(request: Request, response: Response, user: OAuth2PasswordRequestForm):
    existing_user = get_collection_users(request).find_one({"username": user.username})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found"
        )
    existing_user = User(**existing_user)
    existing_user = jsonable_encoder(existing_user)

    correct_pswd = verify_password(user.password, existing_user["password"])
    if not existing_user or not correct_pswd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    encoded_jwt = create_jwt_set_cookies(str(existing_user["_id"]), response)

    return encoded_jwt


def logout(response: Response):
    response.delete_cookie("access_token")


def follow_unfollow_user(request: Request, id: ObjectId, current_user: User):
    if id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow/unfollow yourself.",
        )

    user_to_modify = get_collection_users(request).find_one({"_id": id})
    if not user_to_modify or not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )

    is_following = id in current_user.following

    if is_following:
        get_collection_users(request).update_one(
            {"_id": id}, {"$pull": {"followers": current_user.id}}
        )
        get_collection_users(request).update_one(
            {"_id": current_user.id}, {"$pull": {"following": id}}
        )
        return {"detail": "User unfollowed successfully"}

    else:
        get_collection_users(request).update_one(
            {"_id": id}, {"$push": {"followers": current_user.id}}
        )
        get_collection_users(request).update_one(
            {"_id": current_user.id}, {"$push": {"following": id}}
        )
        return {"detail": "User followed successfully"}


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
