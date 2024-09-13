from sqlalchemy.orm import Session
import models
import schemas


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        responsible_person_id=task.responsible_person_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task: models.Task, task_update: schemas.TaskUpdate):
    update_values = task_update.dict(exclude_unset=True)

    for key, value in update_values.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
    return task


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
