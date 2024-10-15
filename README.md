# Task Scheduler Application

A Flask-based Task Scheduler application that allows users to manage their tasks efficiently. Users can create, read, update, and delete their tasks.

## Features
- **User Authentication**: Register and log in using JSON Web Tokens (JWT).
- **Task Management**: Create, read, update, and delete tasks.
- **Task Reminders**: Set reminders for tasks.
- **Time Tracking**: Track the time spent on tasks.
- **Admin Features**: Admin users can manage any task in the system.

## Technologies Used
- **Flask**: Web framework for building the REST APIs.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-JWT-Extended**: For user authentication.
- **SQLite**: Lightweight database for storing user and task data.
- **pytest**: Testing framework for unit tests.
- **pytest-cov**: Coverage reporting for tests.

## Installation
### Prerequisites
- Python 3.10.13 (Version used)
- pip

### Run Application
1. Run the following command in your terminal:
   ```bash
   python app.py
 Note: The database tables will be created automatically when you run the application for the first time.
## API Endpoints

### Register New User
- **URL**: `POST /api/auth/register`
- **Request Body**: 
  ```json
  { 
    "username": "string", 
    "email": "string", 
    "password": "string" 
  }
### Login
- **URL**: `POST /api/auth/login`
- **Request Body**: 
  ```json
  { 
    "username": "string", 
    "password": "string" 
  }
- **Response**;
  ```json
  {
   "access_token": "string"
  }
### Create Task
- **URL**: `POST /api/tasks/`
- **Request Body**: 
  ```json
  {
     "title": "string",
     "description": "string",
      "reminder_time": "YYYY-MM-DDTHH:MM:SS"
  }

### Get All Task;
 - **URL**: `GET /api/tasks/`
### Update Task:
- **URL**: `PUT /api/tasks/`
- **Request Body**: 
  ```json
  {
     "title": "string",
     "description": "string",
      "reminder_time": "YYYY-MM-DDTHH:MM:SS"
  }
### Delete Task:
- **URL**: DELETE /api/tasks/{task_Id}
