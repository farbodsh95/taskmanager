Project Description
    This Django-based Task Manager allows users to manage tasks, including creating, viewing, updating, and deleting tasks. The app provides two primary components: tasks and api apps, which handle separate functionalities. It supports RESTful API endpoints for task management and includes user authentication for secure access. Bootstrap is used for a simple UI interface.

Features
    User Authentication: Secure login system using Django’s default authentication.
    Task Management: Full CRUD (Create, Read, Update, Delete) functionality for tasks.
    REST API: API endpoints for managing tasks with token-based authentication.
    Task Search: Search tasks by title or description.
    Bootstrap UI: A clean interface to view and manage tasks.

Prerequisites
    Ensure you have the following installed:
        Python 3.x
        pip (Python package manager)
        Django

Installation and Setup
    1. Clone the repository:
        Run `git clone <repository_url>`
        Run `cd taskmanager`
    
    2. Set up a Virtual Environment:
        Run `python -m venv venv`
        Run `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`
    
    3. Install the required dependencies:
        Run `pip install -r requirements.txt`

    4. Set Environment Variables:
        Create a .env file in the project root based on .env.sample.
            TEST_USER_NAME= # a username of your choice for testing
            TEST_USER_PASSWORD= # a password of your choice for testing
            DEBUG= # Set to False in production
            ALLOWED_HOSTS= # Depends on the production's ip and domain

    5. Database Migrations:
        Run `python manage.py migrate`

    6. Create a Superuser:
        Run `python manage.py createsuperuser`

    7. Run the Development Server:
        Run `python manage.py runserver`

    8. Visiting the Application:
        Visit http://127.0.0.1:8000/login and use your username & password to login and see the application.

    9. Running Tests (Optional):
        Run `python manage.py test`

Project Structure
    The project now contains two main Django apps:
        tasks: Manages the core task functionalities, including creating, viewing, editing, and deleting tasks.
        api: Provides RESTful API endpoints for task management with token-based authentication.

Using the Application
    HTML Views
        The following views are accessible via the web interface:
            Task List View: Lists tasks for the logged-in user with search functionality.
            Task Detail View: Shows details of a selected task.
            Create Task: Allows users to create a new task.
            Edit Task: Enables users to modify tasks they created.
            Delete Task: Allows users to delete tasks they created.

    API Endpoints
        The application provides the following RESTful API endpoints, requiring token-based authentication via JWT (JSON Web Tokens) for secure access.
            1. Authentication Endpoints
                Login
                    Endpoint: /api/login/
                    Methods: POST
                    Description: Returns a pair of access and refresh tokens for authentication.
                    Example Request: curl -X POST http://127.0.0.1:8000/api/login/ -d "username=yourusername&password=yourpassword"
                Token Refresh
                    Endpoint: /api/refresh/
                    Methods: POST
                    Description: Provides a new access token using the refresh token.
            2. Task Management Endpoints
                List and Create Tasks
                    Endpoint: /api/tasks/
                    Methods: GET, POST
                    Description:
                        GET: Retrieves a list of all tasks available to the authenticated user.
                        POST: Allows an authenticated user to create a new task. The task will automatically be associated with the logged-in user.
                            Example request body:   
                                                {
                                                    "title": <your_task_title>, # String
                                                    "description": <your_task_description>, # String
                                                    "status": <your_task_status>, # String, available options are "Pending", "In Progress" and "Completed".
                                                }
                Retrieve, Update, and Delete a Task
                    Endpoint: /api/tasks/<int:pk>/
                    Methods: GET, PUT, PATCH, DELETE
                    Description:
                        GET: Retrieves details of a specific task by id.
                        PATCH: Partially updates the task’s fields. You only need to send the fileds that need to be updated. Only the task’s owner can perform this action.
                        DELETE: Deletes a specific task. Only the task’s owner can perform this action. A success message will be returned upon deletion.
                
                Note: All tasks endpoints require authentication with a valid access token in the request header as Authorization: Bearer <token>.
                API Usage Example:
                    For authenticated requests to the tasks API, use the access token obtained from the /api/login/ endpoint. Include the token in the request headers as follows:
                    curl -X GET http://127.0.0.1:8000/api/tasks/ -H "Authorization: Bearer <access_token>"