from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from .models import Users

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'username', ]


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=allauth_settings.USERNAME_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        if not allauth_settings.USERNAME_REQUIRED:
            raise serializers.ValidationError(_("A user is already registered with this username."))
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        user.type = self.cleaned_data.get('type')
        user.save()
        return user


class UserPasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_password(self, request, data):
        if check_password(data.get('old_password', False), request.user.password):
            if not data.get('new_password', False) or not data.get('confirm_password', False):
                raise serializers.ValidationError(_("`new password` or `confirm password` is not exists."))
            if data['new_password'] != data['confirm_password']:
                raise serializers.ValidationError(_("The two password fields didn't match."))
            return data
        else:
            raise serializers.ValidationError(_("`old password` is not correct."))

    def save(self, user, data):
        user.set_password(data.get('new_password'))
        user.save()
