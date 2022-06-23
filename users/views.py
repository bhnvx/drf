from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Users
from .serializers import UserSerializer, CustomRegisterSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Users.objects.all()

    def perform_create(self, serializer):
        serializer.save(self.request)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CustomRegisterSerializer
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class UserGetTokenAndLoginViewSet(GenericViewSet):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Users.objects.all()

    def Login(self):
        pass

    def GetToken(self):
        data = self.request.user.id
        token = Token.objects.get(user_id=data)
        res = {'token': token.key}
        return response.Response(res, status=status.HTTP_200_OK)