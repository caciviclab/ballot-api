# flake8: noqa

import os

import dj_database_url

from .common import *


DATABASES['default'] = dj_database_url.config()

SECRET_KEY = os.environ.get('SECRET_KEY', None)

if not SECRET_KEY:
    raise Exception('SECRET_KEY environment variable must be set for heroku configuration.')
