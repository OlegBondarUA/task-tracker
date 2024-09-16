from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from database import Base
import enum


class UserRole(enum.Enum):
    USER_DEFAULT = "user"
    USER_ADMIN = "admin"


class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"


task_executors = Table(
    'task_executors', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER_DEFAULT)

    tasks: Mapped[List["Task"]] = relationship(secondary=task_executors, back_populates='executors')
    responsible_tasks: Mapped[List["Task"]] = relationship(back_populates='responsible_person')


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority: Mapped[int] = mapped_column(Integer, default=1)

    responsible_person_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    responsible_person: Mapped["User"] = relationship(back_populates="responsible_tasks")
    executors: Mapped[List["User"]] = relationship(secondary=task_executors, back_populates='tasks')