from fastapi import FastAPI

from routes.user import user_router, user_create_router
from routes.task import task_router
from routes.tag import tag_router
from routes.token import auth_router
from db.database import init_db

init_db()

app = FastAPI()

app.include_router(user_router)
app.include_router(user_create_router)
app.include_router(task_router)
app.include_router(tag_router)
app.include_router(auth_router)
