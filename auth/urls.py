from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserInfoViewSet


router = DefaultRouter()
router.register('', UserInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='login'),
]