from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, PostSerializer, PostActionSerializer
from .models import Post, PostAction
from .permissions import IsOwnerOrReadOnly, IsStaffOrTargetUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.AllowAny
    ]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = PostAction.objects.all()
    serializer_class = PostActionSerializer

    def create(self, request, *args, **kwargs):
        """
        Four possible scenarios for user/vote for a given post.:
        1. User did not vote before and new vote is a like:
            - Behavior: Register like and increase number of likes by one.
        2. User did not vote before and new vote is an unlike:
            - Behavior: Do nothing, as you cannot unlike a post you didnt first like.
        3. User voted before, and new vote is a like:
            - Behavior: Do nothing, as you cannot like a post that you already like.
        4. User voted before, and new vote is an unlike:
            - Behavior: Delete current vote, decrease number of likes by one.
        """
        user_id = int(request.user.id)
        post_id = int(request.data["post_id"])
        vote = int(request.data["action_type"])

        existing_actions_for_post = PostAction.objects.filter(post_id=post_id).all()
        existing_users_for_post = [int(action.user_id.id) for action in existing_actions_for_post]

        if user_id not in existing_users_for_post:
            if vote:
                # Scenario 1
                serializer = PostActionSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    # return Response(status=status.HTTP_303_SEE_OTHER, data={"message": str(serializer.data)})
                    post = Post.objects.filter(id=post_id).first()
                    post.number_of_likes += 1
                    post.save()
                    return Response(serializer.data)
                else:
                    return Response(data="Serializer call for PostAction is invalid.", status=status.HTTP_409_CONFLICT)
            else:
                # Scenario 2
                return Response(data="Cannot unlike post that is not liked.", status=status.HTTP_200_OK)
        else:
            existing_action_by_user = None
            for action in existing_actions_for_post:
                if int(action.user_id.id) == user_id:
                    existing_action_by_user = action
                    break

            existing_vote_by_user = int(existing_action_by_user.action_type)
            if vote == 0 and existing_vote_by_user == 1:
                # Scenario 4
                post = Post.objects.filter(id=post_id).first()
                post.number_of_likes -= 1
                post.save()
                existing_action_by_user.delete()
                return Response(data="Unlike successful.", status=status.HTTP_200_OK)
            elif vote == 1:
                # Scenario 3
                return Response(data="Already liked post.", status=status.HTTP_200_OK)
            else:
                # Scenario 2
                return Response(data="Cannot unlike post that is not liked.", status=status.HTTP_200_OK)

