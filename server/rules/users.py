from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from db.models.user import User
from bson import ObjectId



crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return crypt.verify(plain_password, hashed_password)

def get_password_hash(password):
    return crypt.hash(password)

def get_collection_users(request: Request):
  return request.app.database["users"]

def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    existing_user = get_collection_users(request).find_one({"email": user["email"]})
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email address is already in use")
    
    user["password"] = get_password_hash(user["password"])
    
    new_user = get_collection_users(request).insert_one(user)
    created_user = get_collection_users(request).find_one({"_id": new_user.inserted_id})
    return created_user


def list_users(request: Request, limit: int):
    users = list(get_collection_users(request).find(limit = limit))
    return users


def find_user(request: Request, id: ObjectId):
    if (user := get_collection_users(request).find_one({"_id": id})):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")


def delete_user(request: Request, id: ObjectId):
    deleted_user = get_collection_users(request).delete_one({"_id": id})

    if deleted_user.deleted_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")