from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *


router = routers.DefaultRouter()

router.register('signup', UserViewSet)
router.register('get_user_from_token', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
