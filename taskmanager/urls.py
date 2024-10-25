from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
