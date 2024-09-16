from pydantic import BaseModel
from typing import Optional, List
from models import UserRole, TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[int] = 1
    responsible_person_id: Optional[int] = None
    executors: Optional[list[int]] = []


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[int] = 1
    responsible_person_id: Optional[int] = None
    executors: Optional[list[int]] = []


class TaskUpdate(TaskBase):
    pass


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class Task(TaskBase):
    id: int
    executors: Optional[List[int]]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.USER_DEFAULT


class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True
