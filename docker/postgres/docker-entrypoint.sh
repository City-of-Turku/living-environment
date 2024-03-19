#!/bin/sh
set -e

for ext in postgis hstore; do
    psql --username "$POSTGRES_USER" "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS $ext"
done
