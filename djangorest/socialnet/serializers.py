from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SocialnetUser, Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.user.username')

    class Meta:
        model = Post
        fields = ('created', 'creator', 'number_of_likes', 'content')


class SocialnetUserSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = SocialnetUser
        fields = ('first_name', 'last_name', 'email', 'posts')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.user.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.user.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


