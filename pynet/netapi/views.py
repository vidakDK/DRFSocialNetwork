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

    # def get_permissions(self):
    #     return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]


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
        If user did not vote for a given post, register his vote as a new instance
        in the PostAction relationship table.
        """
        user_id = int(request.user.id)
        post_id = int(request.data["post_id"])
        vote = int(request.data["action_type"])

        #return Response(status=status.HTTP_303_SEE_OTHER, data={"message": post_id})
        existing_actions_for_post = PostAction.objects.filter(post_id=post_id).all()
        existing_users_for_post = [int(action.user_id.id) for action in existing_actions_for_post]
        # return Response(status=status.HTTP_303_SEE_OTHER, data={"message": str(existing_users_for_post)})

        if user_id not in existing_users_for_post:
            # return Response(status=status.HTTP_303_SEE_OTHER, data={"message": "user_id={}, existing_users={}".format(user_id, str(existing_users_for_post))})
            if vote:
                # Number of likes increases if it is an upvote;
                # otherwise it stays the same as user cannot unlike a post that he did not like first.
                serializer = PostActionSerializer(data=request.data)
                if serializer.is_valid():
                    return Response(status=status.HTTP_303_SEE_OTHER, data={"message": str(serializer.data)})
                    post = Post.objects.filter(id=post_id).first()
                    post.number_of_likes += 1
                    post.save()
                    # serializer.save()
                    return Response(serializer.validated_data)
                else:
                    return Response(data="Serializer call for PostAction is invalid.", status=status.HTTP_409_CONFLICT)

        else:
            existing_action_by_user = None
            for action in existing_actions_for_post:
                if int(action.user_id.id) == user_id:
                    existing_action_by_user = action
                    break

            existing_vote_by_user = int(existing_action_by_user.action_type)
            if vote == 0 and existing_vote_by_user == 1:
                # This means that the new action is an unlike.
                post = Post.objects.filter(id=post_id).first()
                post.number_of_likes -= 1
                post.save()
                existing_action_by_user.delete()
                return Response(data="Unlike successful.", status=status.HTTP_200_OK)
            elif vote == 1:
                return Response(data="Already liked post.", status=status.HTTP_200_OK)
            else:
                return Response(data="Cannot unlike post that is not liked.", status=status.HTTP_200_OK)

