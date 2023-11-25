from fastapi import FastAPI

from routes.user import user_router, user_create_router
from routes.task import task_router
from routes.group import group_router
from routes.tag import tag_router
from routes.token import auth_router
from db.database import init_db

init_db()

app = FastAPI(
    redoc_url="/docs",
    docs_url=None,
    version="1.0",
    root_path="/api/v1",
)

app.include_router(user_router)
app.include_router(user_create_router)
app.include_router(task_router)
app.include_router(tag_router)
app.include_router(auth_router)
app.include_router(group_router)
