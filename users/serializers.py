from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        return user

    class Meta:
        model = Users
        fields = ['id', 'username']