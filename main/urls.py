from django.urls import path, include
from rest_framework import routers

from main.views import UserViewSet

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users/(?P<year>[0-9]+)', UserViewSet)

urlpatterns = [

    # --- URLs pour Django-REST-Framework --- :
    path('', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls')),

]
