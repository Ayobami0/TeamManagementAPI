from fastapi import FastAPI

from routes.user import user_router
from routes.task import task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
