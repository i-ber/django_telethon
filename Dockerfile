FROM python:alpine
LABEL authors="iber"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем обновления и необходимые модули
RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

# Обновление pip python
RUN pip install --upgrade pip

# Установка пакетов для проекта
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app

# Удаляем зависимости билда
RUN apk del .build-deps

# Копирование проекта
COPY . .

RUN chmod +x manage.py

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
