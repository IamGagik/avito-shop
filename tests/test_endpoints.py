import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

# Создаем тестовый клиент
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Создаем таблицы в БД для тестирования
    Base.metadata.create_all(bind=engine)
    yield
    # По окончании тестов удаляем таблицы
    Base.metadata.drop_all(bind=engine)


def test_auth_and_get_info():
    # 1. Регистрируем пользователя / получаем токен
    auth_payload = {"username": "user1", "password": "password1"}
    response = client.post("/api/auth", json=auth_payload)
    assert response.status_code == 200, f"Response: {response.json()}"
    token = response.json().get("token")
    assert token, "Не получен токен при аутентификации"

    # 2. Получаем информацию о пользователе с помощью токена
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/info", headers=headers)
    assert response.status_code == 200, f"Response: {response.json()}"
    data = response.json()
    assert "coins" in data, "В ответе отсутствует поле coins"
    assert isinstance(data["coins"], int), "coins должен быть числом"


def test_purchase_item():
    # Регистрируем пользователя для покупки
    auth_payload = {"username": "buyer", "password": "buyerpass"}
    response = client.post("/api/auth", json=auth_payload)
    token = response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Покупаем мерч, например, "t-shirt" (его цена 80)
    response = client.get("/api/buy/t-shirt", headers=headers)
    assert response.status_code == 200, f"Response: {response.json()}"

    # Проверяем, что количество монет уменьшилось
    response_info = client.get("/api/info", headers=headers)
    data_info = response_info.json()
    assert data_info[
        "coins"
        ] == 1000 - 80, f"Ожидалось 920 монет, получено {data_info['coins']}"


def test_send_coin():
    # Регистрируем двух пользователей: отправитель и получатель
    auth_payload_sender = {"username": "sender", "password": "senderpass"}
    response_sender = client.post("/api/auth", json=auth_payload_sender)
    token_sender = response_sender.json().get("token")
    headers_sender = {"Authorization": f"Bearer {token_sender}"}

    auth_payload_receiver = {
        "username": "receiver", "password": "receiverpass"
        }
    response_receiver = client.post("/api/auth", json=auth_payload_receiver)
    token_receiver = response_receiver.json().get("token")
    headers_receiver = {"Authorization": f"Bearer {token_receiver}"}

    # Отправляем 100 монет от отправителя к получателю
    send_payload = {"toUser": "receiver", "amount": 100}
    response_send = client.post(
        "/api/sendCoin",
        json=send_payload,
        headers=headers_sender)
    assert response_send.status_code == 200, f"Respons: {response_send.json()}"

    # Проверяем, что у отправителя монеты уменьшились,
    # а у получателя увеличились
    info_sender = client.get("/api/info", headers=headers_sender).json()
    info_receiver = client.get("/api/info", headers=headers_receiver).json()
    assert info_sender["coins"] == 1000 - 100, f"""Отправитель должен иметь 900
    монет, получено {info_sender['coins']}"""
    assert info_receiver["coins"] == 1000 + 100, f"""Получатель должен иметь
    1100 монет, получено {info_receiver['coins']}"""
