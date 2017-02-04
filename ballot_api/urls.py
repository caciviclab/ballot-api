from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from ballot.views import CandidateViewSet, ElectionViewSet

router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'elections', ElectionViewSet)

schema_view = get_swagger_view(title='Open Disclosure Ballot API')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', schema_view),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
