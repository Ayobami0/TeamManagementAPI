from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class User(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    new_password: str


class UserInDB(UserBase):
    id: int


class UserInDBWithPass(UserInDB):
    hashed_password: str
