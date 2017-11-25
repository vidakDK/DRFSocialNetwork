from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsSuperOrNormalUser
from .serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User

    def get_permissions(self):
        # allow non-authentificated user to create via POST requests
        return (AllowAny() if self.request.method == 'POST' else IsSuperOrNormalUser()),

