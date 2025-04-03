# Task Managing API

This is a simple task managing API built with FastAPI and SQLModel. 
It allows users to create, read, update, and delete tasks.

### Features

- JWT authentication
- CRUD operations for tasks
- User registration and authentication
- Task filtering and sorting


## Models

### User
- id: UUID
- name: str
- email: str
- password: str

### Task
- id: UUID
- Description: str
- completed: bool
- user_id: UUID


## Endpoints

### User Endpoints

- `GET /user/`: Filter users by params
- `GET /user/me`: Get current user information
- `POST /user/create`: Register a new user
- `PUT /user/{user_id}`: Update user information

### Task Endpoints

- `GET /task/all`: Get All tasks from user using JWT token
- `GET /task/`: Filter tasks by params
- `DELETE /task/delete/{task_id}`: Delete task by task_id
- `PUT /task/{task_id}`: Update task by task_id
- `POST /task`: Create a new task

### Authentication Endpoints

- `POST /auth/token`: User Login



