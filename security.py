import os
from typing import Type

from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from models import User, UserRole
from dependencies import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Отримання поточного користувача з токеном
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user


# Перевірка наявності ролі адміністратора
def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.USER_ADMIN:
        raise HTTPException(
            status_code=403, detail="Not enough privileges"
        )
    return current_user
