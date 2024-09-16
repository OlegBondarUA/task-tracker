from sqlalchemy.orm import Session
import models
import schemas
from utils import send_email_mock


def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        responsible_person_id=user_id
    )

    if task.executors:
        executors = db.query(models.User).filter(models.User.id.in_(task.executors)).all()
        new_task.executors = executors
        for executor in executors:
            send_email_mock(executor.email, new_task.title, new_task.status)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    task_response = schemas.Task(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        status=new_task.status,
        priority=new_task.priority,
        responsible_person_id=new_task.responsible_person_id,
        executors=[executor.id for executor in new_task.executors]
    )
    return task_response


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None

    # Створення словника для оновлення
    update_data = {
        "title": task_update.title,
        "description": task_update.description,
        "status": task_update.status,
        "priority": task_update.priority,
        "responsible_person_id": task_update.responsible_person_id
    }

    # Оновлення полів
    for key, value in update_data.items():
        if value is not None:
            setattr(db_task, key, value)

    # Оновлення executors окремо
    if task_update.executors is not None:
        executors = db.query(models.User).filter(models.User.id.in_(task_update.executors)).all()
        db_task.executors = executors

        # Відправка email кожному executor
        for executor in executors:
            send_email_mock(executor.email, db_task.title, db_task.status.value)  # Використовуємо .value для статусу

    db.commit()
    db.refresh(db_task)

    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "status": db_task.status.value,  # Використовуємо .value для статусу
        "priority": db_task.priority,
        "responsible_person_id": db_task.responsible_person_id,
        "executors": [user.id for user in db_task.executors]
    }


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
    return task


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
