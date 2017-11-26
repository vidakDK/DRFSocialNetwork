from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import detail_route

from .serializers import SocialnetUserSerializer, PostSerializer
from .models import SocialnetUser, Post
from .permissions import IsOwnerOrReadOnly


class SocialnetUserViewSet(viewsets.ModelViewSet):
    queryset = SocialnetUser.objects.all()
    serializer_class = SocialnetUserSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)
