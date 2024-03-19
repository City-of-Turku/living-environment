# Living Environment

This learning platform aims to inform young citizens about the maintenance of the urban city environment, as well as show them the way to influence their environment.

## Development

### Creating requirements

* Run `pip-compile requirements.in`
* Run `pip-compile requirements-dev.in`

### Updating requirements

* Run `pip-compile --upgrade requirements.in`
* Run `pip-compile --upgrade requirements-dev.in`

### Installing requirements

* Run `pip install -r requirements.txt`
* Run `pip install -r requirements-dev.txt`

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S living_environment
    sudo -u postgres createdb -O living_environment living_environment

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER living_environment CREATEDB;"

### Daily running

* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `npm run build`
* Run `python manage.py runserver 0:8000`

## Production

### Environments

Uses django-environ for configurations, create .env-file in your project dir to override settings.


Environment variable | Type | Description
--- | --- | ---
FEEDBACK_SYSTEM_URL | str | url of feedback system used for student signup for voluntary tasks
FEEDBACK_SERVICE_CODE | str | service code used for voluntary tasks. Code can be found using same url as for feedback system but with requests.json replaced with services.json
FEEDBACK_API_KEY | str | api key for the feedback requests
CORS_ORIGIN_WHITELIST | list | A list of origin hostnames that are authorized to make cross-site HTTP requests.
FRONTEND_APP_URL | str | absolute site url used as a link from admin page
STATIC_URL | str | absolute or relative site url used for serving static files
MEDIA_URL | str | absolute or relative site url used for serving media files
DATABASE_URL | str | Database URL with credentials
STATIC_ROOT | str | Path to static files
MEDIA_ROOT | str | Path to media files


### Starting with docker-compose

.env file example:
```
POSTGRES_USER=example_user
POSTGRES_PASSWORD=example_password
POSTGRES_DB=example_database
DATABASE_URL=postgis://example_user:example_password@db:5432/example_database

ALLOWED_HOSTS=example.domain.org
```

Build and start container (production):
```sh
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --force-recreate --build --detach --no-start
docker compose -f docker-compose.yml -f docker-compose.prod.yml start
```

Build and start container (development):
```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --force-recreate --build --detach --no-start
docker compose -f docker-compose.yml -f docker-compose.dev.yml start
```


Apply migrations and create a superuser
```sh
docker compose run --env DATABASE_HOST=db --rm api apply_migrations
docker compose run --env DATABASE_HOST=db --rm api createsuperuser
```


## Running tests

- Set the `DEBUG` environment variable to `1`.
- Run `py.test .`
