from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app import crud, schemas
from app.db import SessionLocal

router = APIRouter()

# Конфигурация JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Зависимость для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Зависимость для получения текущего пользователя по JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Не удалось проверить учетные данные")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Не удалось проверить учетные данные")
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


@router.post("/auth", response_model=schemas.AuthResponse)
def login(auth_data: schemas.AuthRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, auth_data.username)
    if not user:
        # Если пользователя нет — создаём автоматически
        user = crud.create_user(db, auth_data.username, auth_data.password)
    else:
        # Проверяем пароль
        if not crud.verify_password(auth_data.password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Неверные учетные данные")

    # Формируем данные для токена
    token_data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}
