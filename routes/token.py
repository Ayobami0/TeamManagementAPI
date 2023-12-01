from datetime import timedelta
from typing_extensions import Annotated
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
import config
from models.user import User, UserInDBWithPass

from security.token import Token
from security.utils import authenticate_user, create_access_token, get_current_user

auth_router = APIRouter(tags=["Auth"], prefix="/login")


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Username represents the email address here. This is what is specified
    # by the openapi specfication.
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/user/me", response_model=UserInDBWithPass)
async def read_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
