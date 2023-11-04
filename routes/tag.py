from fastapi import APIRouter

tag_router = APIRouter(prefix="/tags", tags=["Tags"])


@tag_router.get("/")
async def get_tags():
    pass


@tag_router.post("/")
async def add_tag():
    pass


@tag_router.delete("/")
async def remove_tag(id):
    pass


@tag_router.post("/{tag_id}/tasks/{task_id}")
async def add_task_to_tag(task_id, tag_id):
    pass


@tag_router.delete("/{tag_id}/tasks/{id}")
async def remove_task_from_tag(task_id, tag_id):
    pass
