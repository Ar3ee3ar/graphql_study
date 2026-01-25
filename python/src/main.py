import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from contextlib import asynccontextmanager

# from db.fake_db import fake_users_db
# from routers.auth.routes import router as auth_router
from routers.user.routes import get_user, verify_api_key, insert_api_key
from routers.user.models import User, ApiUserBase
from routers.user.jwt_handler import SECRET_KEY, ALGORITHM
from routers.user.routes import router as user_router
from db.main import create_db_and_tables
from routers.graphql.main import graphql_app

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token_ask") # schema that will use for get token (call /token_ask)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application start up: Initialize database")
    await create_db_and_tables()
    yield
    # print("Application shutdown: shutdown database")
    # await shutdown()
    # yield

app = FastAPI()
# app.include_router(auth_router)
app.include_router(user_router)

class TokenData(BaseModel):
    username: str | None = None

class QueryRequest(BaseModel):
    question: str


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    return user

@app.get('/reqKey')
def request_apiKey(user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    api_key = uuid.uuid4()
    return {"api_key": api_key}

@app.post('/regKey')
def register_apiKey(api:ApiUserBase, user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    message = insert_api_key(api)
    return {"message": message}

app.include_router(graphql_app, prefix="/graphql")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
