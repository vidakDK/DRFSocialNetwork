from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('number_of_likes', 'content', 'owner')


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'posts')
        write_only_fields = ('password',)

