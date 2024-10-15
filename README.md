Task Scheduler Application
    A Flask-based Task Scheduler application that allows users to manage their tasks efficiently. Users can create, read, update, and delete their tasks.
    Features:
        User Authentication: Register and log in using JSON Web Tokens (JWT).
        Task Management: Create, read, update, and delete tasks.
        Task Reminders: Set reminders for tasks.
        Time Tracking: Track the time spent on tasks.
        Admin Features: Admin users can manage any task in the system
    Technologies Used:
        Flask: Web framework for building the REST APIs.
        Flask-SQLAlchemy: ORM for database interactions.
        Flask-JWT-Extended: For user authentication.
        SQLite: Lightweight database for storing user and task data.
        pytest: Testing framework for unit tests.
        pytest-cov: Coverage reporting for tests.
  Installation:
      Prerequisites:
        Python 3.10.13 (Version i used)
        pip
  Run Application :
      Python app.py
      Note: The database tables will be created automatically when you run the application for the first time.
API Endpoints:
    Register New user:
        URL: POST /api/auth/register
        Request Body: { "username": "string", "email": "string", "password": "string" }
    Login:
      URL: POST /api/auth/login
      Request Body: { "username": "string", "password": "string" }
      Response : { "access_token": "token" }
    Create Task
      URL: POST /api/tasks/
      Request body: { "title": "string", "description": "string", "reminder_time": "YYYY-MM-DDTHH:MM:SS", "user_id": 1 }
    Get All task:
      URL: GET /api/tasks/
    Get Task:
      URL: GET /api/tasks/{task_Id}
    Update Task:
      URL: PUT /api/tasks/{task_Id}
      Request Body: { "title": "string", "description": "string", "reminder_time": "YYYY-MM-DDTHH:MM:SS", "user_id": 1 }
    Delete Task:
      URL: DELETE /api/tasks/{task_Id}