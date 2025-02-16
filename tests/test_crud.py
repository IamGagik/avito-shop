import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app import crud


@pytest.fixture(scope="function")
def db_session():
    # Создаем in-memory базу данных
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(db_session):
    user = crud.create_user(db_session, "unittest_user", "testpass")
    assert user.username == "unittest_user"
    assert user.coins == 1000
    # Проверяем, что пароль валидируется корректно
    assert crud.verify_password("testpass", user.hashed_password)
