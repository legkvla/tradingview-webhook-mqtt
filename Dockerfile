FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app/app.py
#COPY ca.crt /app/ca.crt
#RUN  chmod 644 /etc/redis/tls/ca.crt

COPY ca.crt /app/ssl/ca.crt
#COPY redis.crt /app/ssl/redis.crt
#COPY redis.key /app/ssl/redis.key
RUN mkdir -p /app/ssl && chmod 644 /app/ssl/*.crt

CMD [ "uvicorn", "app:app", "--port", "8080", "--host", "0.0.0.0" ]
