from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

import ballot.views as ballot_views
import gsheets.views as gsheets_views

router = routers.SimpleRouter()
#router.register(r'candidates', ballot_views.CandidateViewSet)
router.register(r'elections', ballot_views.ElectionViewSet)
router.register(r'candidates', gsheets_views.CandidateViewSet)

schema_view = get_swagger_view(title='Open Disclosure Ballot API')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', schema_view),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
