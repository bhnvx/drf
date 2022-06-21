from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response

from .models import Users
from .serializers import UserSerializer, CustomRegisterSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Users.objects.all()

    def perform_create(self, serializer):
        serializer.save(self.request)

    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CustomRegisterSerializer
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
