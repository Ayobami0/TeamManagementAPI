from typing import List
from fastapi import APIRouter
from models.task import Task

from models.user import User, UserCreate, UserInDB

user_router = APIRouter(tags=["user"], prefix="/users")

fake_user_db = [
    UserInDB(
        id=0,
        username="User 1",
        email="user1@email.com",
        hashed_password="user1password",
    ),
    UserInDB(
        id=1,
        username="User 2",
        email="user2@email.com",
        hashed_password="user2password",
    ),
    UserInDB(
        id=2,
        username="User 3",
        email="user3@email.com",
        hashed_password="user3password",
    ),
    UserInDB(
        id=3,
        username="User 4",
        email="user4@email.com",
        hashed_password="user4password",
    ),
    UserInDB(
        id=4,
        username="User 5",
        email="user5@email.com",
        hashed_password="user5password",
    ),
]


@user_router.get("/", response_model=List[User])
async def get_users():
    return fake_user_db


@user_router.get("/{id}", response_model=User)
async def get_user_by_id(id: int):
    user: UserInDB | None = None
    for u in fake_user_db:
        if u.id == id:
            user = u
    return user


@user_router.post("/create", response_model=User)
async def create_user(user: UserCreate):
    if user:
        for usr in fake_user_db:
            if usr.id == user:
                return usr
        fake_user_db.append(user)

    return user


@user_router.put("/{id}/update", response_model=User)
async def update_user(id: int, user: UserInDB):
    for idx, usr in enumerate(fake_user_db):
        if usr.id == id:
            fake_user_db.remove(usr)
            fake_user_db.insert(idx, user)
            user = usr
    return user


@user_router.delete("/{id}/delete", response_model=User)
async def delete_user(id: int):
    user = None
    for usr in fake_user_db:
        if usr.id == id:
            fake_user_db.remove(usr)
            user = usr
    return user


@user_router.get("/{id}/tasks", response_model=Task)
async def get_user_tasks(id: int):
    pass
