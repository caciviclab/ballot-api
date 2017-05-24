# flake8: noqa

import os

import dj_database_url

from .common import *

DEBUG = False


if 'ALLOWED_HOSTS' not in os.environ:
    raise Exception('ALLOWED_HOSTS environment variable must be set to a comma-separated list of host names for heroku configuration.')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', ['*'])


if 'DATABASE_URL' not in os.environ:
    raise Exception('DATABASE_URL environment variable must be set for heroku configuration.')

DATABASES['default'] = dj_database_url.config()


if 'SECRET_KEY' not in os.environ:
    raise Exception('SECRET_KEY environment variable must be set for heroku configuration.')

SECRET_KEY = os.environ.get('SECRET_KEY')
