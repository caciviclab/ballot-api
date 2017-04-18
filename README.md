[![Build
Status](https://travis-ci.org/caciviclab/ballot-api.svg?branch=master)](https://travis-ci.org/caciviclab/ballot-api)

# Ballot API

This app is inspired by the schema defined in the [Voter Information
Project](https://www.votinginfoproject.org/) in order to provide ballot data for
California.

## Prequisites

- Python 3
- [PostgreSQL](https://www.postgresql.org/)


## Setup

    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

And open your browser to http://localhost:8000


## Development

Please don't forget to run the tests.

    $ flake8
    $ python manage.py test


## Deployment

The ballot-api can easily be deployed to Heroku. After creating an initial app
in Heroku, you'll want to set these environment variables. `DATABASE_URL` should
be set automatically after enabling the PostgreSQL add-on.

| Environment variable     | Description | Example |
| ------------------------ | ----------- | ------- |
| `ALLOWED_HOSTS`          | Comma-separated list of host names for the app | caciviclab-ballot-api.herokuapp.com |
| `DATABASE_URL`           | [Database connection URL](https://pypi.python.org/pypi/dj-database-url) (set by PostgreSQL add-on) |  postgresql://user:password@hostname:port/database_name?options |
| `DJANGO_SETTINGS_MODULE` | Settings module to use for Django | ballot_api.settings.heroku |
| `SECRET_KEY`             | Django secret key | a-random-string-of-50-characters |


### Continuous deployment

The `caciviclab-ballot-api` is deployed continuously to Heroku via Travis by merging to
the `master` branch. Once tests and linting checks are good, `master` is
deployed and any pending migrations will be run.
