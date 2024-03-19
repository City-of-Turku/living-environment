FROM python:3.11-slim-bullseye as setup

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV STATIC_ROOT=/var/www/static/ MEDIA_ROOT=/var/www/media/

RUN adduser --disabled-login --no-create-home --gecos '' arkiymparisto
WORKDIR /srv/app
COPY . .
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential netcat gettext python-dev libpq-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r deploy/requirements.txt --no-cache-dir

RUN mkdir -p /srv/logs && chown arkiymparisto:arkiymparisto /srv/logs

RUN python manage.py compilemessages
RUN python manage.py collectstatic --no-input

ENTRYPOINT ["./docker-entrypoint.sh"]

FROM setup as production
USER arkiymparisto
ENV TIER=prod
ENV PRODUCTION=1
EXPOSE 8000/tcp
