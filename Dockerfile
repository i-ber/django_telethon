FROM python:3.11.5
LABEL authors="iber"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
#RUN apt-get update && apt-get add libpq
RUN pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
