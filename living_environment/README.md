# Living Environment

Hello! I am the Living Environment project.
My developers are lazy and haven't written a good README.

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

    sudo -u postgres createuser -P -R -S living_environment  # use password `living_environment`
    sudo -u postgres createdb -O living_environment living_environment

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER living_environment CREATEDB;"

### Daily running

* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `npm run build`
* Run `python manage.py runserver 0:8000`

## Running tests

* Set the `DEBUG` environment variable to `1`.
* Run `py.test`.
