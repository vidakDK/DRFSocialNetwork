from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),

]

