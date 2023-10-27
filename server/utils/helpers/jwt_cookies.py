from fastapi import Response
from datetime import timedelta
from jose import jwt

from config.config_api import settings
from utils.helpers.datetime_helpers import datetime_now


def create_jwt_set_cookies(
    id: str, res: Response, expires_delta: timedelta | None = None
):
    to_encode = dict(id=id)

    if expires_delta:
        expire = datetime_now() + expires_delta
    else:
        expire = datetime_now() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    res.set_cookie(
        key="jwt",
        value=encoded_jwt,
        httponly=True,
        domain="127.0.0.1",
        max_age=expire.strftime("%a, %d-%b-%Y %T GMT"),
        expires=expire.strftime("%a, %d-%b-%Y %T GMT"),
        samesite="strict",
    )

    return encoded_jwt
