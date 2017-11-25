from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .permissions import IsSuperOrNormalUser
from .serializers import SocialnetUserSerializer, PostSerializer
from .models import SocialnetUser, Post


class SocialnetUserList(generics.ListCreateAPIView):
    queryset = SocialnetUser.objects.all()
    serializer_class = SocialnetUserSerializer


class SocialnetUserDetail(generics.RetrieveAPIView):
    queryset = SocialnetUser.objects.all()
    serializer_class = SocialnetUserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

