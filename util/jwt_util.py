import datetime

import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException


def create_jwt(account_id: int):
    return get_jwt_secret(account_id)


def decode_jwt(access_token: str):
    if len(access_token) == 0:
        return None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, "../.env"))
    SECRET = os.environ.get("JWT_SECRET")
    account = 0
    try:
        account = jwt.decode(access_token, SECRET, algorithms='HS512')['account_id']
    except:
        raise HTTPException(status_code=401, detail="Token Expired")
    return account


def get_jwt_secret(account_id: int):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, "../.env"))
    SECRET = os.environ.get("JWT_SECRET")
    access_token = jwt.encode(
        {
            "account_id": account_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=17280000)
        },
        SECRET,
        algorithm="HS512"
    )
    refresh_token = jwt.encode(
        {
            "account_id": account_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=40000000)
        },
        SECRET,
        algorithm="HS512"
    )
    return access_token, refresh_token