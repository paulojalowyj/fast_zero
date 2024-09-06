from datetime import datetime, timedelta

from jwt import encode, decode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from fast_zero.settings import Settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fast_zero.database import get_session

from fastapi import Depends

from http import HTTPException, HTTPStatus

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    # Adiciona um tempo para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, Settings().JWT_SECRET, algorithm=Settings().JWT_ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    payload = decode(token, Settings().JWT_SECRET, algorithms=Settings().JWT_ALGORITHM)

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, Settings().JWT_SECRET)
        username: str = payload.get('sub')
        if not id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
