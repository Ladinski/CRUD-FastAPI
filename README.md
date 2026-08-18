# Task API

A CRUD Task Management API built with **FastAPI** and **PostgreSQL**. The project implements CRUD (Create, Read, Update, Delete) operations for managing tasks and includes automatically generated interactive API documentation using Swagger UI.

The application uses a layered architecture that separates the API, service, repository, and database layers. PostgreSQL runs inside Docker, and the complete application stack can be started using Docker Compose.

## Features

- Create, retrieve, update, and delete tasks
- Persistent task storage using PostgreSQL
- PostgreSQL running in Docker
- Docker Compose for starting the API and database together
- Persistent database storage using a Docker volume
- Database connection configuration using environment variables
- Automatic database table creation
- Automatic seeding of example tasks when the table is empty
- Filter tasks by completion status using SQL `WHERE`
- Search tasks by title using SQL
- Pagination using SQL `LIMIT` and `OFFSET`
- Alphabetical task sorting using SQL `ORDER BY`
- Task statistics using SQL `COUNT()`
- Layered backend architecture
- Interactive Swagger documentation

## Architecture

The application follows a layered architecture:

```text
Client
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
```

The router handles HTTP requests and responses, the service layer contains application logic and validation, and the repository handles database operations.

The project previously used SQLite for persistence. When PostgreSQL was introduced, the API routes and service layer did not need to change. The storage implementation was changed in the repository layer while keeping the same API behavior.

This demonstrates the separation between the API and data layers: clients can continue using the same endpoints regardless of how the application stores its data.

## Requirements

To run the complete application:

- Docker Desktop
- Docker Compose

For local Python development:

- Python 3.10+
- FastAPI
- Uvicorn
- Psycopg
- python-dotenv

## Installation

Clone the repository:

```bash
git clone https://github.com/Ladinski/CRUD-FastAPI.git
cd CRUD-FastAPI
```

## Environment Variables

Database configuration is stored using environment variables.

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks
```

The `.env` file is excluded from Git because it can contain credentials and environment-specific configuration.

An `.env.example` file is included in the repository to show which environment variables are required.

## Running with Docker Compose

The entire application stack can be started with one command:

```bash
docker compose up
```

Docker Compose starts:

- The FastAPI application
- The PostgreSQL database

To build the application again after changing dependencies or the Dockerfile:

```bash
docker compose up --build
```

Once the application is running, open:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

To stop the stack:

```bash
docker compose down
```

## Eval Results

Prompt version: `task-analyze-v1`

Date: `2026-08-18`

Result: `4/8` correct (`50.0%`)

Failed cases:
- "Finish my FastAPI assignment tonight" was classified as `work` instead of `study`.
- "Prepare slides for the client meeting tomorrow" was given `medium` priority instead of `high`.
- "Buy groceries this weekend" was given `medium` priority instead of `low`.
- "Review database notes before class" was classified as `work` instead of `study`.

This gives me a baseline for future prompt changes. The main weakness is distinguishing `study` from `work` and applying consistent priority rules.

## Cost / Usage Example

The project currently uses the local Ollama model `gemma3:1b`, so there is no per-request provider charge.

Example model call:

```json
{
  "prompt_version": "task-analyze-v1",
  "model": "gemma3:1b",
  "input_tokens": 377,
  "output_tokens": 51,
  "duration_ms": 1129.7,
  "repair": false
}


## Authentication

This API uses Supabase Auth for user authentication.

Users can:

- Sign up
- Log in
- Receive JWT access and refresh tokens
- Access protected routes using a Bearer token
- Log out

Protected routes verify the access token through Supabase before returning private data.

## Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Required variables:

```env
DATABASE_URL=postgres://postgres:YOUR_PASSWORD@localhost:5432/tasks
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY

## PostgreSQL Database

The application uses PostgreSQL for persistent task storage.

PostgreSQL runs inside a Docker container and stores its data in a named Docker volume:

```text
taskdata
```

The `tasks` table is automatically created if it does not already exist.

When the table is empty, three example tasks are inserted:

```text
Update to do list
Setup Flyrank profile
Go to the gym
```

### Database Schema

The `tasks` table contains:

| Column | Type | Description |
| ------ | ---- | ----------- |
| `id` | SERIAL | Primary key and unique task ID |
| `title` | TEXT | Task title |
| `done` | BOOLEAN | Whether the task is completed |

## Persistence

PostgreSQL data is stored using a Docker named volume instead of inside the temporary container filesystem.

I verified persistence by:

1. Starting the application with `docker compose up`.
2. Creating a new task through the API.
3. Confirming the task appeared using `GET /tasks`.
4. Stopping the application and database using `docker compose down`.
5. Starting the stack again using `docker compose up`.
6. Running `GET /tasks` again.

The task was still present after the application and database containers were restarted, confirming that the PostgreSQL data persisted through the Docker volume.

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/` | Returns basic API information |
| GET | `/health` | Returns the API health status |
| GET | `/tasks` | Returns tasks |
| GET | `/tasks/{task_id}` | Returns a specific task by ID |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/{task_id}` | Updates an existing task |
| DELETE | `/tasks/{task_id}` | Deletes a task |
| GET | `/tasks/stats` | Returns task statistics |

The `GET /tasks` endpoint also supports filtering, searching, and pagination.

## Search

Tasks can be searched by title using the `search` query parameter.

Example:

```text
GET /tasks?search=milk
```

The search is performed in the database rather than filtering an in-memory Python list.

## Filter by Completion Status

Tasks can be filtered using the `done` query parameter.

Completed tasks:

```text
GET /tasks?done=true
```

Incomplete tasks:

```text
GET /tasks?done=false
```

## Pagination

The `GET /tasks` endpoint supports pagination using the `limit` and `offset` query parameters.

Example:

```text
GET /tasks?limit=2&offset=2
```

This request skips the first two tasks and returns the next two.

Real-world APIs typically avoid returning every record at once because datasets can become very large. Pagination reduces the amount of data transferred, lowers memory usage, and keeps response times manageable as the dataset grows.

## Task Statistics

The statistics endpoint returns the number of total, completed, and open tasks.

```text
GET /tasks/stats
```

Example response:

```json
{
  "total": 3,
  "done": 2,
  "open": 1
}
```

The statistics are calculated using SQL `COUNT()` queries against PostgreSQL.

## Example curl Request

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example response:

```http
HTTP/1.1 200 OK
content-type: application/json

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

## Database Verification

The PostgreSQL database can be inspected directly from the running Docker container.

For example:

```bash
docker exec -it crudfastapiv2-db-1 psql -U postgres -d tasks
```

Inside PostgreSQL, the tasks can be viewed with:

```sql
SELECT * FROM tasks;
```

Example:

```text
 id |         title          | done
----+------------------------+------
  1 | Update to do list      | t
  2 | Setup Flyrank profile  | t
  3 | Go to the gym          | f
```

### Database Screenshot

Add a screenshot here showing the PostgreSQL `tasks` table or `psql` output.

```markdown
![PostgreSQL tasks table](images/postgres-database.png)
```

## Swagger Documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

After starting the application, Swagger is available at:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test the CRUD endpoints directly from the browser.

Add your Swagger screenshot here:

```markdown
![Swagger documentation](images/swagger.png)
```

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- Psycopg
- Docker
- Docker Compose
- Pydantic
- Uvicorn
- python-dotenv
- Swagger UI / OpenAPI

## Project Evolution

The project was developed incrementally:

1. Built a CRUD API using in-memory task storage.
2. Added filtering, search, pagination, and statistics.
3. Replaced in-memory storage with SQLite for persistence.
4. Replaced SQLite with PostgreSQL while preserving the API interface.
5. Ran PostgreSQL inside Docker with persistent volume storage.
6. Containerized the FastAPI application.
7. Combined the API and database using Docker Compose.

The transition from SQLite to PostgreSQL primarily affected the repository layer. The routes and service logic remained unchanged, demonstrating the benefit of separating application logic from persistence.

## Author

Borjan Ladinski