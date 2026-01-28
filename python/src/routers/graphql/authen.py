from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from fastapi import Depends, FastAPI, HTTPException, status, Security
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status, Security
from typing import Annotated
from pydantic import BaseModel

from routers.user.routes import get_user
from routers.user.jwt_handler import SECRET_KEY, ALGORITHM
from authen_check import TokenData

async def authen_ql(req: Request):
    user = None
    authen_req = req.headers.get("Authorization")
    if authen_req.startswith("Bearer "):
        token = authen_req.split(" ")[1]
    else:
        # If someone sent a token without "Bearer ", or wrong format
        token = authen_req

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    # print(f"username: {token_data.username}")
    user = get_user(username=token_data.username)
    # print(f"user: {user}")
    if user is None:
        raise credentials_exception
    return {
        "request": req,
        "user": user
    }