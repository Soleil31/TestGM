import logging
import uuid
from jose import jwt, JWTError
from fastapi import Depends
from typing import Annotated
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.utils.user_utils import unix_time_millis
from settings.loader import SECRET_KEY
from app.constants.token_constants import (
    ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS, OAUTH2_URL
)
from app.exceptions.token_exceptions import InvalidAuthenticationCredentials, TokenExpired
from database import crud
from app.schemas.user_schemas import UserSchema


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=OAUTH2_URL,
    scheme_name="Login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


async def create_access_token(sub: str) -> str:
    to_encode = {
        "sub": sub,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "token_type": "access",
    }
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


async def create_refresh_token(sub: str) -> str:
    to_encode = {
        "sub": sub,
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "token_type": "refresh",
    }
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    await crud.create_refresh_token(
        token=encoded_jwt,
        exp=int(to_encode.get("exp")),
        iat=int(to_encode.get("iat")),
        jti=to_encode.get("jti"),
        user_id=int(to_encode.get("sub")),
    )

    return encoded_jwt


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> UserSchema:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        user_id = str(payload.get("sub"))

        if user_id is None:
            raise InvalidAuthenticationCredentials()

        token_expired: int = payload.get("exp")
        now = datetime.now(timezone.utc)
        now_unix = await unix_time_millis(now)

        if token_expired < now_unix:
            raise TokenExpired()

    except JWTError as e:
        logging.error(f"JWTError: {e}")
        raise InvalidAuthenticationCredentials()

    user: UserSchema = await crud.read_user_by_user_id(user_id=int(user_id))

    return user
