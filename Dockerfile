# Используем минимальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем утилиты для ping
RUN apt-get update && apt-get install -y iputils-ping

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта
COPY . .

# Используем ENTRYPOINT для корректного вызова команд
ENTRYPOINT ["python", "app.py"]
