from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
import rest_auth.serializers

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
        )
        return post


class UserSerializer(serializers.HyperlinkedModelSerializer):
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
    user_id = serializers.ReadOnlyField(source='user_id.id')

    class Meta:
        model = PostAction
        fields = ('user_id', 'post_id', 'action_type')
        read_only_fields = ('user_id',)

    def create(self, validated_data):
        user = self.context['request'].user
        post_action = PostAction.objects.create(
            user_id=user,
            **validated_data
        )
        return post_action


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        # fields['email'] = fields['username']
        del fields['username']
        return fields

    # def validate(self, attrs):
    #     # attrs['username'] = attrs['email']
    #     # del attrs['username']
    #     return super(LoginSerializer, self).validate(attrs)