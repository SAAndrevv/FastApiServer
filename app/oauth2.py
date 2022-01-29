from jose import JWTError, jwt

from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas
from .config import settings
from .db import database, models
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SHARED_TOKEN_EXPIRE_MINUTES = settings.shared_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_shared_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=SHARED_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id_user")
        role: str = payload.get("role")

        if id is None:
            raise credentials_exceptions

        token_data = schemas.UserToken(id_user=id,
                                       role=role)
        try:
            data = payload.get("data")
            token_data.data = data
        except Exception:
            pass


    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user_data(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    # user = db.query(models.User).filter(models.User.id_user == token.id_user).first()

    return token  # user
