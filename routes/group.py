from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_202_ACCEPTED
from db.crud.admins import demote, is_admin, promote
from db.crud.chats import (
    delete_chat_from_group_in_db,
    get_chat_by_id_in_db,
    send_chat_to_group_in_db,
)
from db.crud.groups import (
    add_user_to_group_in_db,
    check_user_in_group,
    create_new_group,
    get_group_by_id_db,
    remove_group_in_db,
    remove_user_from_group_in_db,
    update_group_in_db,
)
from db.crud.users import read_user_by_id_from_db
from db.factories import as_GroupDB
from models.chats import Chat, ChatInDB
from models.group import GroupCreate, GroupUpdate

from security.utils import get_current_user

group_router = APIRouter(
    tags=["Groups"], prefix="/groups", dependencies=[Depends(get_current_user)]
)


@group_router.post("")
async def create_group(group: GroupCreate):
    group_id = create_new_group(group)

    new_group = get_group_by_id_db(group_id)
    return as_GroupDB(new_group)


@group_router.put("/{id}")
async def update_group(id, update: GroupUpdate):
    if get_group_by_id_db(id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )
    update_group_in_db(id, update)

    return as_GroupDB(get_group_by_id_db(id))


@group_router.delete(
    "/{id}",
    responses={HTTP_202_ACCEPTED: {"message": "Deleted"}},
)
async def delete_group(id: int):
    if get_group_by_id_db(id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )
    remove_group_in_db(id)


@group_router.post("/{id}/admin/{admin_id}/promote")
async def promote_user(id: int, admin_id: int, user_id: int):
    group = get_group_by_id_db(id)
    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    if not is_admin(admin_id, id):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not autorized to perform this action.",
        )
    if is_admin(user_id, id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"User is an admin.",
        )

    if read_user_by_id_from_db(user_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist.",
        )
    if not check_user_in_group(id, user_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} \
is not part of this group",
        )
    promote(user_id, id)

    return group


@group_router.delete("/{id}/admin/{admin_id}/demote")
async def demote_user(id: int, admin_id: int, user_id: int):
    group = get_group_by_id_db(id)
    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    if not is_admin(admin_id, id):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not autorized to perform this action.",
        )
    if not is_admin(user_id, id):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"User is not an admin.",
        )

    if read_user_by_id_from_db(user_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist.",
        )
    if not check_user_in_group(id, user_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} \
is not part of this group",
        )
    demote(user_id, id)

    return group


@group_router.post("/{id}/admin/{admin_id}")
async def add_user_to_group(id: int, admin_id: int, user_id: int):
    group = get_group_by_id_db(id)
    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    if not is_admin(admin_id, id):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not autorized to perform this action.",
        )

    if read_user_by_id_from_db(user_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist.",
        )

    add_user_to_group_in_db(id, user_id)
    return group


@group_router.delete("/{id}/admin/{admin_id}")
async def remove_user_from_group(id: int, admin_id: int, user_id: int):
    group = get_group_by_id_db(id)
    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    if not is_admin(admin_id, id):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not autorized to perform this action.",
        )

    if read_user_by_id_from_db(user_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist.",
        )
    if not check_user_in_group(id, user_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} \
is not part of this group",
        )
    remove_user_from_group_in_db(id, user_id)

    return group


@group_router.post("/{id}/message")
async def send_message(id: int, chat_message: Chat):
    group = get_group_by_id_db(id)
    if chat_message.group_id != id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Mismatch group.",
        )

    if read_user_by_id_from_db(chat_message.sender_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {chat_message.sender_id} does not exist.",
        )

    if not check_user_in_group(id, chat_message.sender_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {chat_message.sender_id} \
is not part of this group",
        )
    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    send_chat_to_group_in_db(chat_message)

    return group


@group_router.delete("/{id}/message")
async def remove_message(id: int, chat_message: ChatInDB):
    group = get_group_by_id_db(id)

    if not get_chat_by_id_in_db(chat_message.id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_message.id} does not exist.",
        )

    if chat_message.group_id != id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Mismatch group.",
        )

    if read_user_by_id_from_db(chat_message.sender_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {chat_message.sender_id} does not exist.",
        )

    if not check_user_in_group(id, chat_message.sender_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {chat_message.sender_id} \
is not part of this group",
        )

    if group is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} does not exist.",
        )

    delete_chat_from_group_in_db(chat_message)

    return group
