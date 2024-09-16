from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models import UserRole, TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[int] = 1
    responsible_person_id: Optional[int] = None
    executors: Optional[List[int]] = []

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    title: str


class TaskUpdate(TaskBase):
    pass


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class Task(TaskBase):
    id: int


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER_DEFAULT


class User(UserBase):
    id: int
    role: UserRole
