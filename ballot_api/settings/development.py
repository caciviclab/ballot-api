# flake8: noqa
from .common import *

try:
    from local_settings import *
except ImportError:
    pass
