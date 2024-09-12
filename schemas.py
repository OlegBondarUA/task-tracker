from pydantic import BaseModel
from typing import List, Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "TODO"
    priority: Optional[int] = 1
    responsible_person: Optional[str] = None
    executors: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
