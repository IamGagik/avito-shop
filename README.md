# 🛍 Avito Shop API

**An internal merchandise store API for Avito employees — where team members can exchange coins and purchase goods.**

---

## 📌 **1. Project Description**

This service allows users to:

- Authenticate and receive a JWT token  
- Purchase products using internal coins  
- Transfer coins to other employees  
- View coin balance and transaction history  

---

## 🚀 **2. Running the Project**

### 📦 **2.1. Local Launch (without Docker)**

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Make sure PostgreSQL is running** and a database named `avito_shop` exists. If not, create it:

```sql
CREATE DATABASE avito_shop;
```

3. **Set environment variables**  
Create a `.env` file in the root and add:

```env
SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/avito_shop"
```

4. **Run the app:**

```bash
uvicorn app.main:app --reload
```

5. **Open Swagger UI:**  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🐳 **2.2. Local Launch with Docker**

> Make sure **Docker** and **Docker Compose** are installed and running.

Check versions:

```bash
docker --version
docker-compose --version
```

1. **Update your `.env` file**:

```env
SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@db:5432/avito_shop"
```

2. **Update `app/db.py` to use environment variable:**

```python
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/avito_shop"
)
```

3. **Build and run the containers:**

```bash
docker-compose up --build
```

4. **Check that containers are running:**

```bash
docker ps
```

5. **Access Swagger UI:**  
👉 [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 💪 **3. Running Tests**

> ✅ **Important**: Set the correct local DB URL in `.env` before running tests:

```env
SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/avito_shop"
```

Then run tests:

```bash
pytest
```
