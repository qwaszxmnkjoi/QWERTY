FROM python:3.11-slim-buster

COPY /app /opt/app
WORKDIR /opt/app

RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install libpq-dev gcc git libmagic-dev python3-dev gettext build-essential
RUN pip install -r requirements.txt

COPY ./docker/python/entrypoint.sh /opt/app/entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
