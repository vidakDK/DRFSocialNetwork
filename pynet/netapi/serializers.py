from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from .models import Post, PostAction


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'number_of_likes', 'content', 'owner')
        read_only_fields = ('number_of_likes',)

    def create(self, validated_data):
        tmp_post = validated_data
        user = None

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        post = Post.objects.create(
            owner=user,
            content=tmp_post['content'],
            # number_of_likes=tmp_post['number_of_likes'],
        )
        return post


class UserSerializer(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'posts')
        write_only_fields = ('password',)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class PostActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAction
        fields = '__all__'

    # def create(self, validated_data):
    #     """
    #     If user did not vote for a given post, register his vote as a new instance
    #     in the PostAction relationship table.
    #     """
    #     instance = None
    #     user = validated_data["user"]
    #     post = validated_data["post"]
    #     vote = validated_data["action_type"]
    #
    #     existing_actions_for_post = PostAction.objects.filter(post=post)
    #     # existing_users_for_post = existing_actions_for_post.user
    #     existing_users_for_post = [action.user for action in existing_actions_for_post]
    #
    #     if user not in existing_users_for_post:
    #         if vote:
    #             # Number of likes increases if it is an upvote;
    #             # otherwise it stays the same as user cannot unlike a post that he did not like first.
    #             instance = self.Meta.model(**validated_data)
    #             post.number_of_likes += 1
    #             post.save()
    #             instance.save()
    #     else:
    #         existing_action_by_user = None
    #         for action in existing_actions_for_post:
    #             if action.user == user:
    #                 existing_action_by_user = action
    #                 break
    #
    #         existing_vote_by_user = existing_action_by_user.action_type
    #         if vote == 0 and existing_vote_by_user == 1:
    #             # This means that the new action is an unlike.
    #             post.number_of_likes -= 1
    #             post.save()
    #             existing_action_by_user.delete()
    #
    #     return instance


