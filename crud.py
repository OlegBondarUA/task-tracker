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
        _send_emails_to_executors(executors, new_task.title, new_task.status.value)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return _task_response(new_task)


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_fields = {
        "title": task_update.title,
        "description": task_update.description,
        "status": task_update.status,
        "priority": task_update.priority,
        "responsible_person_id": task_update.responsible_person_id
    }
    _update_task_fields(db_task, update_fields)

    if task_update.executors is not None:
        executors = db.query(models.User).filter(models.User.id.in_(task_update.executors)).all()
        db_task.executors = executors
        _send_emails_to_executors(executors, db_task.title, db_task.status.value)

    db.commit()
    db.refresh(db_task)

    return _task_response(db_task)


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
    return task


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def _update_task_fields(task, update_fields):
    """Оновлення полів задачі, якщо значення не None"""
    for field, value in update_fields.items():
        if value is not None:
            setattr(task, field, value)


def _send_emails_to_executors(executors, task_title, task_status):
    """Відправка email усім виконавцям"""
    for executor in executors:
        send_email_mock(executor.email, task_title, task_status)


def _task_response(task):
    """Підготовка відповіді після створення/оновлення задачі"""
    return schemas.Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        responsible_person_id=task.responsible_person_id,
        executors=[executor.id for executor in task.executors]
    )
