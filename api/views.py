from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from tasks.models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Requires token for viewing and creating

    def perform_create(self, serializer):
        # Task creation is tied to the logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Allow viewing all tasks for all authenticated users
        return Task.objects.all()


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires token

    def get_object(self):
        # Fetch the task object
        task = super().get_object()

        # Check if the current user is the owner for update/delete operations
        if (
            self.request.method in ["PUT", "PATCH", "DELETE"]
            and task.user != self.request.user
        ):
            raise PermissionDenied(
                "You do not have permission to edit or delete this task."
            )

        return task

    def patch(self, request, *args, **kwargs):
        # Allow partial update on fields
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Fetch the task object and check permissions
        task = self.get_object()

        # Perform the delete operation
        self.perform_destroy(task)

        # Return a custom response with a success message
        return Response(
            {"message": "Task deleted successfully."}, status=status.HTTP_200_OK
        )
