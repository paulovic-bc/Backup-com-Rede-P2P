from django.urls import include, path
from rest_framework import routers

from .views import NodeViewSet

router = routers.DefaultRouter()
router.register("", NodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
