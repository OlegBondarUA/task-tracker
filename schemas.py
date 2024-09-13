from pydantic import BaseModel
from typing import Optional
from models import UserRole, TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[int] = 1
    responsible_person_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True
