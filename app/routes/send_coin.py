from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.routes.auth import get_current_user, get_db

router = APIRouter()


@router.post("/sendCoin")
def send_coin(data: schemas.SendCoinRequest,
              current_user: models.User = Depends(get_current_user),
              db: Session = Depends(get_db)):

    receiver = crud.get_user_by_username(db, data.toUser)
    if not receiver:
        raise HTTPException(
            status_code=400,
            detail="Пользователь получатель не найден")
    try:
        crud.create_coin_transaction(
            db,
            sender=current_user,
            receiver=receiver,
            amount=data.amount)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Монеты успешно переведены"}
