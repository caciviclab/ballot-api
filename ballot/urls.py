from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .admin import api_admin
from .views import CandidateViewSet, ElectionViewSet


router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'elections', ElectionViewSet)

schema_view = get_swagger_view(title='Open Disclosure Ballot API')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', schema_view),
    url(r'^admin/', api_admin.urls),
]
