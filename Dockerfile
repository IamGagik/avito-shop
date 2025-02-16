# Используем официальный образ Python (например, 3.11)
FROM python:3.11-slim

# Отключаем создание файлов .pyc и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Задаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/requirements.txt

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Открываем порт 8080
EXPOSE 8080

# Запускаем приложение через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
