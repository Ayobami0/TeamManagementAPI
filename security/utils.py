from datetime import timedelta, datetime
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing_extensions import Annotated, Union
from db.crud.users import read_user_by_email_from_db

from db.factories import as_UserDB
from security.token import TokenData
import config

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email_address: str, password: str):
    user = read_user_by_email_from_db(email_address)

    if not user:
        return False
    user = as_UserDB(user)
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email_address: str = payload.get("sub")
        if email_address is None:
            raise credentials_exception
        token_data = TokenData(email_address=email_address)
    except JWTError:
        raise credentials_exception
    user = read_user_by_email_from_db(token_data.email_address)
    if user is None:
        raise credentials_exception
    return as_UserDB(user)
