from django.conf.urls import url
from .admin import api_admin

urlpatterns = [
    url(r'^admin/', api_admin.urls),
]
