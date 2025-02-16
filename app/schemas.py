from pydantic import BaseModel, Field
from typing import List


# Схемы для аутентификации
class AuthRequest(BaseModel):
    username: str = Field(
        ...,
        description="Имя пользователя для аутентификации")
    password: str = Field(
        ...,
        description="Пароль для аутентификации")


class AuthResponse(BaseModel):
    token: str = Field(
        ...,
        description="JWT-токен для доступа к защищенным ресурсам")


# Схемы для информации о пользователе
class InventoryItem(BaseModel):
    type: str = Field(..., description="Тип предмета")
    quantity: int = Field(..., description="Количество предметов")


class CoinHistoryItemReceived(BaseModel):
    fromUser: str = Field(
        ...,
        description="Имя пользователя, который отправил монеты")
    amount: int = Field(
        ...,
        description="Количество полученных монет")


class CoinHistoryItemSent(BaseModel):
    toUser: str = Field(
        ...,
        description="Имя пользователя, которому отправлены монеты")
    amount: int = Field(
        ...,
        description="Количество отправленных монет")


class CoinHistory(BaseModel):
    received: List[CoinHistoryItemReceived] = Field(default_factory=list)
    sent: List[CoinHistoryItemSent] = Field(default_factory=list)


class InfoResponse(BaseModel):
    coins: int = Field(..., description="Количество доступных монет")
    inventory: List[InventoryItem] = Field(default_factory=list)
    coinHistory: CoinHistory = Field(...)


# Схема для перевода монет
class SendCoinRequest(BaseModel):
    toUser: str = Field(
        ...,
        description="Имя пользователя, которому нужно отправить монеты")
    amount: int = Field(
        ...,
        description="Количество монет, которые необходимо отправить")


# Схема для ошибок
class ErrorResponse(BaseModel):
    errors: str = Field(..., description="Сообщение об ошибке")
