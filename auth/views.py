from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import permissions, response

from users.models import Users


class UserInfoViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['get', ]
    queryset = Users.objects.all()

    @action(methods=['GET'], detail=False, url_path="me")
    def info(self, request):
        user = Users.objects.get(id=self.request.user.id)
        return response.Response({"id": user.id, "username": user.username})

