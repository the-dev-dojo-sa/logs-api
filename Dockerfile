# Dockerfile
FROM python:3.10-slim

# Отключаем запись байткода и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем системные зависимости (gcc может понадобиться для сборки некоторых пакетов)
RUN apt-get update && apt-get install -y gcc

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходный код
COPY . /app

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
