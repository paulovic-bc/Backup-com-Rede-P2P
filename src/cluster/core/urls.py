"""
URL configuration for cluster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from core import settings
from django.contrib import admin
from django.urls import include, path
from django.urls.conf import include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path(f"api/{settings.API_MAJOR}/admin/", admin.site.urls),
    path(f"api/{settings.API_MAJOR}/api-auth/", include("rest_framework.urls")),
    path(
        f"api/{settings.API_MAJOR}/schema/", SpectacularAPIView.as_view(), name="schema"
    ),
    path(
        f"api/{settings.API_MAJOR}/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(f"api/{settings.API_MAJOR}/nodes/", include("nodes.urls")),
    path(f"api/{settings.API_MAJOR}/files/", include("files.urls")),
]
