FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование исходного кода
COPY main.py .
COPY fabric.py .
COPY publisher.py .
COPY strategy.py .
COPY strfabric.py .
COPY subscriber.py .

# Точка входа
CMD ["python", "main.py"]