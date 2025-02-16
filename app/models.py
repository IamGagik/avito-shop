from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db import Base


# Пользователь
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    coins: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)

    # Связи: транзакции и покупки
    sent_transactions = relationship(
        "CoinTransaction",
        back_populates="sender",
        foreign_keys='CoinTransaction.from_user_id'
    )
    received_transactions = relationship(
        "CoinTransaction",
        back_populates="receiver",
        foreign_keys='CoinTransaction.to_user_id'
    )
    purchases = relationship("Purchase", back_populates="user")


# Транзакции с монетками (передача монет между пользователями)
class CoinTransaction(Base):
    __tablename__ = "coin_transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship(
        "User",
        back_populates="sent_transactions",
        foreign_keys=[from_user_id])
    receiver = relationship(
        "User",
        back_populates="received_transactions",
        foreign_keys=[to_user_id])


# Покупка мерча
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="purchases")
