from rest_framework.viewsets import ModelViewSet

from .models import Users
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass