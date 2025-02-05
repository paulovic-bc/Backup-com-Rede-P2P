from django.urls import include, path
from rest_framework import routers

from .views import FileDownloadByIdViewSet, FileViewSet

router = routers.DefaultRouter()
router.register("", FileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "download/<int:id>/",
        FileDownloadByIdViewSet.as_view(),
        name="download-file-by-id",
    ),
]
