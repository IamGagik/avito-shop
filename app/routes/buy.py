from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models
from app.routes.auth import get_current_user, get_db

router = APIRouter()


@router.get("/buy/{item}")
def buy_item(item: str, current_user: models.User = Depends(get_current_user),
             db: Session = Depends(get_db)):

    try:
        crud.create_purchase(db, current_user, item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"detail": f"Вы успешно купили {item}"}
