from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SocialnetUser, Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Post
        fields = ('number_of_likes', 'content', 'creator')


class SocialnetUserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True,
                                                queryset=Post.objects.all(),
                                                view_name='post-detail')

    class Meta:
        model = SocialnetUser
        fields = ('first_name', 'last_name', 'email', 'posts')
        write_only_fields = ('password',)

    def create(self, validated_data):
        print(repr(validated_data))
        # handle password:
        password = validated_data.pop('password', None)
        posts = validated_data.pop('posts', None)

        # Create user:
        socialnet_user = self.Meta.model(**validated_data)
        if password is not None:
            socialnet_user.user.set_password(password)

        # Handle posts:
        if posts is not None:
            print(posts)
            for post in posts:
                Post.objects.create(creator=socialnet_user, **post)
        socialnet_user.save()
        return socialnet_user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.user.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


