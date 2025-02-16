from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Список мерча и их цены
MERCH_PRICES = {
    "t-shirt": 80,
    "cup": 20,
    "book": 50,
    "pen": 10,
    "powerbank": 200,
    "hoody": 300,
    "umbrella": 200,
    "socks": 10,
    "wallet": 50,
    "pink-hoody": 500,
}


# Пользовательские операции
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = models.User(
        username=username,
        hashed_password=hashed_password,
        coins=1000
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# Операции с монетками
def create_coin_transaction(db: Session, sender: models.User,
                            receiver: models.User, amount: int):

    if sender.coins < amount:
        raise Exception("Недостаточно монет для перевода")
    sender.coins -= amount
    receiver.coins += amount
    transaction = models.CoinTransaction(
        from_user_id=sender.id,
        to_user_id=receiver.id,
        amount=amount)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


# Покупка мерча
def create_purchase(db: Session, user: models.User, item: str):
    if item not in MERCH_PRICES:
        raise Exception("Товар не найден")
    price = MERCH_PRICES[item]
    if user.coins < price:
        raise Exception("Недостаточно монет для покупки")
    user.coins -= price
    purchase = models.Purchase(user_id=user.id, item=item)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


def get_username_by_id(db: Session, user_id: int) -> str:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user.username if user is not None else "Unknown"


# Получение информации о пользователе
def get_user_info(db: Session, user: models.User):
    # Группируем покупки по типу товара
    inventory_data = (
        db.query(
            models.Purchase.item,
            func.count(models.Purchase.id).label("quantity")).filter(
            models.Purchase.user_id == user.id).group_by(
            models.Purchase.item).all()
    )
    inventory = [
        {"type": item, "quantity": quantity}
        for item, quantity in inventory_data
        ]

    # Получаем историю транзакций
    sent_transactions = db.query(models.CoinTransaction).filter(
        models.CoinTransaction.from_user_id == user.id).all()
    received_transactions = db.query(models.CoinTransaction).filter(
        models.CoinTransaction.to_user_id == user.id).all()

    # Для каждого перенаправляем id в имя пользователя
    # (это можно оптимизировать, но здесь для наглядности)
    coin_history = {
        "received": [
            {"fromUser":
             get_username_by_id(db, int(tx.from_user_id)), "amount": tx.amount}
            for tx in received_transactions
        ],
        "sent": [
            {"toUser":
             get_username_by_id(db, int(tx.to_user_id)), "amount": tx.amount}
            for tx in sent_transactions
        ]
    }

    return {
        "coins": user.coins,
        "inventory": inventory,
        "coinHistory": coin_history
    }
