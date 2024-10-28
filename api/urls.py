from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="task-list-create"),
    path(
        "tasks/<int:pk>/",
        views.TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-retrieve-update-destroy",
    ),
]
