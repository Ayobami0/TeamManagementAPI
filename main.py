from fastapi import FastAPI

from routes.user import user_router, user_create_router
from routes.task import task_router
from routes.group import group_router
from routes.tag import tag_router
from routes.token import auth_router
from db.database import init_db

init_db()

version_prefix = "/api/v1"

app = FastAPI(
    redoc_url="{}/docs".format(version_prefix),
    docs_url=None,
)

app.include_router(user_router, prefix=version_prefix)
app.include_router(user_create_router, prefix=version_prefix)
app.include_router(task_router, prefix=version_prefix)
app.include_router(tag_router, prefix=version_prefix)
app.include_router(auth_router, prefix=version_prefix)
app.include_router(group_router, prefix=version_prefix)
