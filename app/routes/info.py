from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.routes.auth import get_current_user, get_db

router = APIRouter()


@router.get("/info", response_model=schemas.InfoResponse)
def get_info(current_user: models.User = Depends(get_current_user),
             db: Session = Depends(get_db)):

    info = crud.get_user_info(db, current_user)
    return info
