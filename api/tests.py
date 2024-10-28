# api/tests/test_api.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from dotenv import load_dotenv
import os

load_dotenv()


class TaskApiTestCase(TestCase):
    def setUp(self):
        # Load username and password from environment variables
        self.test_username = os.getenv("TEST_USER_NAME")
        self.test_password = os.getenv("TEST_USER_PASSWORD")

        # Create a test user
        self.user = User.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        self.api_client = APIClient()

        # Authenticate to get a token for future requests
        login_response = self.api_client.post(
            reverse("token_obtain_pair"),
            {
                "username": self.test_username,
                "password": self.test_password,
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.token = login_response.data["access"]

        # Set up the token in the client's header for authenticated requests
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Create some test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1", description="Description for task 1", user=self.user
        )
        self.task2 = Task.objects.create(
            title="Test Task 2", description="Description for task 2", user=self.user
        )

    def test_api_task_list(self):
        # Test listing all tasks
        response = self.api_client.get(reverse("task-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test Task 1")
        self.assertEqual(response.data[1]["title"], "Test Task 2")

    def test_api_task_create(self):
        # Test creating a new task
        data = {
            "title": "New Task",
            "description": "Description for new task",
            "status": "Pending",
        }
        response = self.api_client.post(reverse("task-list-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_api_task_retrieve(self):
        # Test retrieving a specific task
        url = reverse("task-retrieve-update-destroy", kwargs={"pk": self.task1.pk})
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task 1")

    def test_api_task_update(self):
        # Test updating a specific task
        url = reverse("task-retrieve-update-destroy", kwargs={"pk": self.task1.pk})
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "status": "In Progress",
        }
        response = self.api_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated description")
        self.assertEqual(updated_task.status, "In Progress")

    def test_api_task_delete(self):
        # Test deleting a specific task
        url = reverse("task-retrieve-update-destroy", kwargs={"pk": self.task1.pk})
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_invalid_login(self):
        # Test with invalid login credentials
        response = self.api_client.post(
            reverse("token_obtain_pair"),
            {
                "username": "wronguser",
                "password": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_without_token(self):
        # Test access to the task list endpoint without token authentication
        self.api_client.credentials()  # Remove token
        response = self.api_client.get(reverse("task-list-create"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
