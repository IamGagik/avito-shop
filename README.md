# 🛍 Avito Shop API

**Сервис для внутреннего магазина мерча Авито, где сотрудники могут обмениваться монетами и приобретать товары.**

---

## 📌 **1. Описание проекта**

Данный сервис позво043bяет:

- Авторизоваться и получать JWT-токен.
- Покупать товары за монеты.
- Передавать монеты другим сотрудникам.
- Просматривать баланс монет и историю транзакций.

---

## 🚀 **2. Запуск проекта**

### **📦 2.1. Локальный запуск (без Docker)**

1. **Установите зависимости**

   ```bash
   pip install -r requirements.txt
   ```

2. **Запустите PostgreSQL**\
   Убедитесь, что у вас запущен PostgreSQL, и создана база данных `avito_shop`. Если её нет, создайте:

   ```sql
   CREATE DATABASE avito_shop;
   ```

### **🛠️ 2.1. Локальный запуск (с Docker)**

Убедитесь, что Docker и Docker Compose установлены
Проверьте, что ваш Docker работает:

```bash
   docker --version
   docker-compose --version
```

Поменяйте .env файл с настройками базы данных

```env
   SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@db:5432/avito_shop"
```

и также поменяйте app/db.py
```db.py
   SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/avito_shop"
    )
```


Соберите и запустите Docker-контейнеры

```bash
   docker-compose up --build
```

Проверьте, что все контейнеры запущены

```bash
   docker ps
```

Проверьте API в браузере
Откройте Swagger-документацию:👉 http://localhost:8080/docs

3. **Настройте переменные окружения**\
   В файле `.env` укажите строку подключения к базе данных:

   ```env
   SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/avito_shop"
   ```

4. **Запустите приложение**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Проверьте API в браузере**\
   Откройте Swagger-документацию по адресу:\
   👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💪 **3. Запуск тестов**

### **🔹 3.1. Запуск тестов локально**

Перед запуском тестов **обязательно** измените `SQLALCHEMY_DATABASE_URL` в `.env`, указав `localhost`:

```env
SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/avito_shop"
```

Затем запустите тесты:

```bash
pytest
```

