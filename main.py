from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import models
import schemas
import crud
from security import get_current_user, get_admin_user
from utils import get_password_hash, verify_password, send_email_mock, create_access_token
from dependencies import get_db
from database import engine


ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)


@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return schemas.Task(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status.value,
        priority=db_task.priority,
        responsible_person_id=db_task.responsible_person_id,
        executors=[executor.id for executor in db_task.executors]
    )


@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_admin_user)):
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.patch("/tasks/{task_id}/status", dependencies=[Depends(get_current_user)])
def update_task_status(task_id: int, status_update: schemas.TaskStatusUpdate, db: Session = Depends(get_db),
                       current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if not _is_authorized_for_task(db_task, current_user):
        raise HTTPException(status_code=403, detail="Not authorized to update the task status")

    db_task.status = status_update.status
    db.commit()
    db.refresh(db_task)

    send_email_mock(current_user.email, db_task.title, db_task.status.value)
    return db_task


@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_admin_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, task=db_task)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, role=user.role, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def _is_authorized_for_task(task: models.Task, user: models.User):
    return task.responsible_person_id == user.id or user.id in [executor.id for executor in task.executors]
