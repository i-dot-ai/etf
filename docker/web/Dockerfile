FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y xvfb xfonts-scalable wkhtmltopdf

RUN python3 -m pip install -U pip setuptools wheel

COPY ./requirements.lock /app/requirements.lock
RUN python3 -m pip install -r /app/requirements.lock --no-cache-dir

COPY ./docker/web/start.sh /start.sh
RUN chmod +x /start.sh

COPY . /app

RUN \
    DJANGO_SETTINGS_MODULE=etf.settings_base \
    DJANGO_SECRET_KEY="temp" \
    python manage.py collectstatic --no-input

WORKDIR /app/

EXPOSE 8000

CMD ["sh","/start.sh"]
