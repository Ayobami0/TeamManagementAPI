from fastapi import FastAPI

from routes.user import user_router
from routes.task import task_router
from routes.tag import tag_router
from db.database import init_db

init_db()

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
app.include_router(tag_router)
