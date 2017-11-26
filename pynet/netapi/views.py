from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer, PostSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly, IsStaffOrTargetUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    def get_permissions(self):
        return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

