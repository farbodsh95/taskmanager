# from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, LoginForm
from django.db.models import Q
from rest_framework import generics, permissions
from .serializers import TaskSerializer


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "task_list_view"
                )  # Redirect to task list or wherever you'd like
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")  # Redirect to the login page after logout


# Task List View (with search functionality)
@login_required(login_url="/login")
def task_list_view(request):
    query = request.GET.get("q")
    if query:
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


# Task Detail View
# (allow non-owners to view, but restrict editing and deleting)
@login_required(login_url="/login")
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


# Task Create View (users can create their own tasks)
@login_required
def task_create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Ensure the task is created by the logged-in user
            task.save()
            return redirect("task_list_view")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


# Task Update View
@login_required(login_url="/login")
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()  # Save the updated task
            return redirect(
                "task_detail_view", pk=task.pk
            )  # Redirect to detail view to show updated task
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})


# Task Delete View
@login_required(login_url="/login")
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list_view")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


# DRF-based API views
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
