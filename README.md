[![Build
Status](https://travis-ci.org/adborden/ballot-api.svg?branch=master)](https://travis-ci.org/adborden/ballot-api)

# Ballot API

This app is inspired by the schema defined in the [Voter Information
Project](https://www.votinginfoproject.org/) in order to provide ballot data for
California.

## Prequisites

- [PostgreSQL](https://www.postgresql.org/)


## Setup

    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

And open your browser to http://localhost:8000
