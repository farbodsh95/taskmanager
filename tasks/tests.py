from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from dotenv import load_dotenv
import os

load_dotenv()


class TaskViewTestCase(TestCase):
    def setUp(self):
        # Load username and password from environment variables
        test_username = os.getenv("TEST_USER_NAME")
        test_password = os.getenv("TEST_USER_PASSWORD")

        # Create a test user and log them in
        self.user = User.objects.create_user(
            username=test_username, password=test_password
        )
        self.client.login(username=test_username, password=test_password)

        # Create some test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1", description="Description for task 1", user=self.user
        )
        self.task2 = Task.objects.create(
            title="Test Task 2", description="Description for task 2", user=self.user
        )

    def test_get_task_list(self):
        response = self.client.get(reverse("task_list_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Task 1", response.content)
        self.assertIn(b"Test Task 2", response.content)

    def test_edit_task(self):
        edit_url = reverse("task_update_view", kwargs={"pk": self.task1.pk})
        updated_data = {
            "title": "Updated Task 1",
            "description": "Updated description for task 1",
            "status": "Pending",
        }
        response = self.client.post(edit_url, updated_data)
        self.assertEqual(
            response.status_code, 302
        )  # Expect redirect after successful edit
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.title, "Updated Task 1")
        self.assertEqual(updated_task.description, "Updated description for task 1")

    def test_delete_task(self):
        delete_url = reverse("task_delete_view", kwargs={"pk": self.task1.pk})
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
        response = self.client.post(delete_url)
        self.assertEqual(
            response.status_code, 302
        )  # Expect redirect after successful delete
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
