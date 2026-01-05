import pydantic

class TaskResponse(pydantic.BaseModel):
    task_id: str
    state: str
    name: str | None = None
    worker: str | None = None
