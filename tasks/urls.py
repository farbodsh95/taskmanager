from django.urls import path
from . import views

urlpatterns = [
    # Existing views
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("tasks/", views.task_list_view, name="task_list_view"),
    path("tasks/<int:pk>/", views.task_detail_view, name="task_detail_view"),
    path("tasks/create/", views.task_create_view, name="task_create_view"),
    path("tasks/<int:pk>/update/", views.task_update_view, name="task_update_view"),
    path("tasks/<int:pk>/delete/", views.task_delete_view, name="task_delete_view"),
    # API views
    path("api/tasks/", views.TaskListCreateAPIView.as_view(), name="task-list-create"),
    path(
        "api/tasks/<int:pk>/",
        views.TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-retrieve-update-destroy",
    ),
]
