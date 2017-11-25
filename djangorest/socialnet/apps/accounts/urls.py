from django.conf.urls import url, patterns, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r'accounts', api.views.UserView, 'list')

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
