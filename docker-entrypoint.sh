#!/bin/bash

set -e

function _log(){
  echo $(date "+%F_%T %Z"): $@
}

if [ -n "$DATABASE_HOST" ]; then
  until nc -z -v -w30 "$DATABASE_HOST" 5432
  do
    _log "Waiting for postgres database connection..."
    sleep 1
  done
  _log "Database is up!"
fi

_log "Running \"Hyvä Arkiympäristö\" entrypoint..."

if [ "$1" = "apply_migrations" ]; then
  _log "Applying database migrations..."
  python manage.py migrate
elif [ "$1" = "run_tests" ]; then
  _log "Running tests..."
  pytest --cov . --doctest-modules
elif [ "$1" = "e" ]; then
  shift
  _log "Executing $@"
  exec "$@"
elif [ "$1" = "createsuperuser" ]; then
  shift
  _log ">> Command: createsuperuser <<"
  python manage.py createsuperuser $@
elif [ "$1" = "uwsgi_http_mode" ]; then
  _log "Starting the uwsgi web server (http mode)"
  uwsgi --ini deploy/uwsgi.ini --http 0.0.0.0:8000 --check-static /var/www
else
  _log "Starting the uwsgi web server (socket mode)"
  uwsgi --ini deploy/uwsgi.ini --socket 0.0.0.0:8000 --check-static /var/www
fi

_log "Hyvä Arkiympäristö entrypoint completed..."
