from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, LoginForm
from django.db.models import Q
from rest_framework import generics, permissions


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("task_list_view")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


# Task List View
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
@login_required(login_url="/login")
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


# Task Create View
@login_required
def task_create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list_view")
    else:
        form = TaskForm()
    return render(request, "tasks/task_create_form.html", {"form": form})


# Task Update View
@login_required(login_url="/login")
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail_view", pk=task.pk)
    else:
        form = TaskForm(instance=task)

    # Render the update template
    return render(request, "tasks/task_update_form.html", {"form": form, "task": task})


# Task Delete View
@login_required(login_url="/login")
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list_view")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
