from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.SocialnetUserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.SocialnetUserDetail.as_view()),
    url(r'^socialnet/posts/$', views.PostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
