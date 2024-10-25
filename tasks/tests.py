# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Task
# from dotenv import load_dotenv
# import os

# load_dotenv()


# class TaskViewTestCase(TestCase):
#     def setUp(self):
#         # Get username and password from environment variables
#         test_username = os.getenv("TEST_USER_NAME")
#         test_password = os.getenv("TEST_USER_PASSWORD")

#         # Create a test user using env variables
#         self.user = User.objects.create_user(
#             username=test_username, password=test_password
#         )
#         self.client.login(username=test_username, password=test_password)

#         # Create some test tasks for the user
#         self.task1 = Task.objects.create(
#             title="Test Task 1", description="Description for task 1", user=self.user
#         )
#         self.task2 = Task.objects.create(
#             title="Test Task 2", description="Description for task 2", user=self.user
#         )

#     def test_get_task_list(self):
#         """Test retrieving task list"""
#         response = self.client.get(
#             reverse("task_list_view")
#         )  # Adjust the URL name if needed
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Test Task 1", response.content)
#         self.assertIn(b"Test Task 2", response.content)

#     def test_edit_task(self):
#         """Test editing a task"""
#         edit_url = reverse("task_update_view", kwargs={"pk": self.task1.pk})
#         updated_data = {
#             "title": "Updated Task 1",
#             "description": "Updated description for task 1",
#             "status": "Pending",
#         }
#         response = self.client.post(edit_url, updated_data)

#         # Ensure the task is updated correctly
#         self.assertEqual(response.status_code, 302)  # Redirect after update
#         updated_task = Task.objects.get(pk=self.task1.pk)
#         self.assertEqual(updated_task.title, "Updated Task 1")
#         self.assertEqual(updated_task.description, "Updated description for task 1")


# def test_delete_task(self):
#     """Test deleting a task"""
#     delete_url = reverse("task_delete_view", kwargs={"pk": self.task1.pk})
#     self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
#     response = self.client.post(delete_url)
#     self.assertEqual(response.status_code, 302)
#     self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from dotenv import load_dotenv
import os

load_dotenv()


class TaskViewTestCase(TestCase):
    def setUp(self):
        # Load username and password from environment variables
        test_username = os.getenv("TEST_USER_NAME")
        test_password = os.getenv("TEST_USER_PASSWORD")

        # Create a test user
        self.user = User.objects.create_user(
            username=test_username, password=test_password
        )
        self.client.login(username=test_username, password=test_password)

        # Set up the API client for DRF tests
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

        # Create some test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1", description="Description for task 1", user=self.user
        )
        self.task2 = Task.objects.create(
            title="Test Task 2", description="Description for task 2", user=self.user
        )

    # Original tests for HTML views
    def test_get_task_list(self):
        """Test retrieving task list view"""
        response = self.client.get(reverse("task_list_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Task 1", response.content)
        self.assertIn(b"Test Task 2", response.content)

    def test_edit_task(self):
        """Test editing a task via view"""
        edit_url = reverse("task_update_view", kwargs={"pk": self.task1.pk})
        updated_data = {
            "title": "Updated Task 1",
            "description": "Updated description for task 1",
            "status": "Pending",
        }
        response = self.client.post(edit_url, updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after update
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.title, "Updated Task 1")
        self.assertEqual(updated_task.description, "Updated description for task 1")

    def test_delete_task(self):
        """Test deleting a task via view"""
        delete_url = reverse("task_delete_view", kwargs={"pk": self.task1.pk})
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    # API tests
    def test_api_task_list(self):
        """Test API endpoint for retrieving task list"""
        response = self.api_client.get(reverse("task-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test Task 1")
        self.assertEqual(response.data[1]["title"], "Test Task 2")

    def test_api_task_create(self):
        """Test API endpoint for creating a task"""
        data = {
            "title": "New Task",
            "description": "Description for new task",
            "status": "Pending",
        }
        response = self.api_client.post(reverse("task-list-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_api_task_retrieve(self):
        """Test API endpoint for retrieving a specific task"""
        url = reverse("task-retrieve-update-destroy", kwargs={"pk": self.task1.pk})
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task 1")

    def test_api_task_update(self):
        """Test API endpoint for updating a task"""
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
        """Test API endpoint for deleting a task"""
        url = reverse("task-retrieve-update-destroy", kwargs={"pk": self.task1.pk})
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
