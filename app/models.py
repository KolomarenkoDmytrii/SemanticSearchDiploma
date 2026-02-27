"""Module with pydantic models."""

import pydantic


class TaskResponse(pydantic.BaseModel):
    """Describes task processing status."""

    task_id: str
    state: str
    name: str | None = None
    worker: str | None = None


class FilesListingResponse(pydantic.BaseModel):
    """Filenames of stored documents."""

    filenames: list[str]


class FileRemovedResponse(pydantic.BaseModel):
    """Response returned upon deleton of a stored document."""

    filename: str
    removed: bool
