# Task API

A simple CRUD Task Management API built with **FastAPI**. This project implements basic CRUD (Create, Read, Update, Delete) operations for managing tasks and includes automatically generated interactive API documentation using Swagger UI.

## Features

* Create tasks
* Retrieve all tasks
* Retrieve a task by ID
* Update existing tasks
* Delete tasks
* Interactive Swagger documentation

## Requirements

* Python 3.10+
* FastAPI
* Uvicorn

## Installation

Clone the repository:

```bash
git clone https://github.com/Ladinski/CRUD-FastAPI.git
cd task-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open your browser:

* API: http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs


## API Endpoints

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| GET    | `/`                | Returns basic API information |
| GET    | `/health`          | Returns the API health status |
| GET    | `/tasks`           | Returns all tasks             |
| GET    | `/tasks/{task_id}` | Returns a specific task by ID |
| POST   | `/tasks`           | Creates a new task            |
| PUT    | `/tasks/{task_id}` | Updates an existing task      |
| DELETE | `/tasks/{task_id}` | Deletes a task                |

## Example curl Output

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example output:

```http
HTTP/1.1 200 OK
date: Thu, 30 Jul 2026 15:00:00 GMT
server: uvicorn
content-type: application/json
content-length: 171

[
  {
    "id": 1,
    "title": "Update to do list",
    "done": true
  },
  {
    "id": 2,
    "title": "Setup Flyrank profile",
    "done": true
  },
  {
    "id": 3,
    "title": "Go to the gym",
    "done": false
  }
]
```

## Swagger Documentation

Insert your Swagger UI screenshot here.

Example:

```
docs/swagger.png
```

```markdown
![Swagger UI](docs/swagger.png)
```

## Technologies Used

* Python
* FastAPI
* Uvicorn
* Pydantic
* Swagger UI (OpenAPI)

## Author

Borjan Ladinski
