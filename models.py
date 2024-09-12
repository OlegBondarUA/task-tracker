from sqlalchemy import Column, Integer, String
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="TODO")
    priority = Column(Integer, default=1)
    responsible_person = Column(String, nullable=True)
    executors = Column(String, nullable=True)
