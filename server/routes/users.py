from fastapi import APIRouter, Body, Request, status
from typing import List
from db.models.user import User

import rules.users as users_rules


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User = Body(...)):  
    return users_rules.create_user(request,user)

@router.get("/", response_description="List users", response_model=List[User])
def list_users(request: Request):
    return users_rules.list_users(request, 100)

@router.get("/{id}", response_description="Get a single user by id", response_model=User)
def find_user(request: Request, id: str):    
    return users_rules.find_user(request, id)


@router.delete("/{id}", response_description="Delete a user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(request: Request, id:str):
    return users_rules.delete_user(request, id)