Project Description

    This Django-based Task Manager allows users to manage tasks, including creating, viewing, updating, and deleting tasks. The app uses Django for its API endpoints, and it includes Bootstrap for UI components. Users can log in to manage their own tasks and view tasks created by others.

Features

    User login system (Django's default authentication).
    CRUD (Create, Read, Update, Delete) functionality for tasks.
    RESTful API endpoints for task management.
    Search functionality for tasks by title or description.
    UI with Bootstrap to handle task-related actions.

Prerequisites

    Before you begin, ensure you have the following installed:
        Python 3.x
        pip (Python package manager)
        Django

Installation and Setup
    1. Clone the repository:
        Run `git clone <repository_url>`
        Run `cd taskmanager`
    
    2. Install the required dependencies:
        Run `pip install -r requirements.txt`

    3. Set Environment Variables:
        Create a .env file in the project root based on the .env.sample file.

    3. Database Migrations:
        Run `python manage.py migrate`

    4. Create a Superuser:
        Run `python manage.py createsuperuser`

    5. Run the Development Server:
        Run `python manage.py runserver`

    6. Visiting the Application:
        Visit http://127.0.0.1:8000/tasks to see the application.

    7. Running Tests (Optional):
        Run `python manage.py test`

Using the Application
    HTML Views
        - Task List View: Displays a list of tasks for the logged-in user, with options to search by title or description.
        - Task Detail View: View task details for a selected task.
        - Create Task: Allows users to create a new task with a title, description, and status.
        - Edit Task: Edit existing tasks created by the logged-in user.
        - Delete Task: Delete tasks created by the user.
        - API Endpoints
            This project provides RESTful API endpoints for managing tasks. API documentation can be accessed at the following endpoints.
            + List and Create Tasks:
                Endpoint: http://127.0.0.1:8000/tasks/
                Methods: GET, POST
                Description:
                GET retrieves all tasks for the authenticated user.
                POST creates a new task.

            + Retrieve, Update, and Delete Task:
                Endpoint: http://127.0.0.1:8000/tasks/<task_id>/
                Methods: GET, PUT, DELETE
                Description:
                GET retrieves details for a specific task.
                PUT updates the task.
                DELETE deletes the task.
                Note: These API endpoints require authentication. Use the DRF's built-in login view at /api-auth/login/ for session-based authentication during testing.