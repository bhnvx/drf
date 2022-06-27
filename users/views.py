from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, authentication, response, status

from .models import Users
from .permissions import IsUser
from .serializers import UserSerializer, CustomRegisterSerializer, UserPasswordResetSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]
    authentication_classes = [authentication.TokenAuthentication, ]
    http_method_names = ['get', 'post', 'patch', 'delete', ]
    queryset = Users.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser(), ]
        elif self.action == 'create':
            return [permissions.AllowAny(), ]
        else:
            return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(self.request)

    def perform_destroy(self, instance):
        instance.delete()
        
    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CustomRegisterSerializer
        self.authentication_classes = None
        return super(UserViewSet, self).create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # ...
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super(UserViewSet, self).destroy(request, *args, **kwargs)
        return response.Response({"msg": "success."}, status=status.HTTP_200_OK)
