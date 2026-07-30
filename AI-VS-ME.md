## AI vs Me

For the bonus stage, I asked Codex to generate the same Task API in a separate `ai-version/` folder. My original hand-built application remained unchanged inside the `app/` folder.

### First AI Prompt

```text
Build a complete Task Management REST API using Python and FastAPI.

Create the entire project only inside the ai-version folder. Do not modify any files outside that folder.

Use a layered architecture with this structure:

ai-version/
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── router.py
│   ├── services/
│   │   └── service.py
│   ├── repositories/
│   │   └── repository.py
│   └── schemas/
│       └── schema.py
├── requirements.txt
└── README.md

Architecture responsibilities:

- router.py handles HTTP routes, query parameters, status codes, and HTTP exceptions.
- service.py contains business logic and validation.
- repository.py handles in-memory task storage and data access.
- schema.py contains Pydantic request and response models.
- main.py creates the FastAPI application and includes the router.

API requirements:

- Use in-memory storage only.
- Do not use a database.
- Use integer task IDs.
- Each task must contain:
  - id: integer
  - title: string
  - done: boolean
- New tasks must default to done = false.
- Titles must not be empty or contain only whitespace.

Implement these five task endpoints:

1. GET /tasks
   - Return all tasks
   - Return status code 200

2. GET /tasks/{task_id}
   - Return one task by ID
   - Return 404 if the task does not exist

3. POST /tasks
   - Create a new task
   - Return status code 201
   - Return 400 if the title is empty or contains only whitespace

4. PUT /tasks/{task_id}
   - Allow partial updates
   - The request may contain title, done, or both
   - Return 404 if the task does not exist
   - Return 400 if the new title is empty or contains only whitespace
   - Return 400 if no fields are provided

5. DELETE /tasks/{task_id}
   - Delete a task
   - Return status code 204
   - Return no response body
   - Return 404 if the task does not exist

Also implement:

- GET /
  - Return basic API information

- GET /health
  - Return {"status": "ok"}

FastAPI requirements:

- Configure the application title, description, and version.
- Add summaries and descriptions for the endpoints.
- Swagger UI must be available at /docs.
- Use APIRouter with the prefix /tasks.
- Use HTTPException and FastAPI status constants.
- Keep HTTP-specific logic in the router layer.
- Keep validation and business rules in the service layer.
- Keep all task storage operations in the repository layer.

Project requirements:

- Add __init__.py files where needed.
- Add a requirements.txt file.
- Add a README.md with installation and run instructions.
- The application must run from inside the ai-version folder using:

uvicorn app.main:app --reload --port 8001

Generate all files only inside ai-version.
Do not edit or delete the existing hand-built application outside ai-version.
```

### Running the AI Version

The AI-generated application started successfully using:

```bash
cd ai-version
uvicorn app.main:app --reload --port 8001
```

Its Swagger documentation was available at:

```text
http://127.0.0.1:8001/docs
```

### What the AI Did Better

The AI added a dedicated `TaskResponse` Pydantic model. It used this model as the `response_model` for the API endpoints, which made the response structure more explicit and improved the generated Swagger documentation. My version returned dictionaries without defining a separate response schema.

The AI also created custom `TaskNotFoundError` and `TaskValidationError` exception classes. This clearly separated missing-resource errors from validation errors. My version used `None`, Boolean return values, and the general `ValueError` exception.

The AI repository stored tasks in a dictionary indexed by task ID:

```python
self._tasks: dict[int, TaskResponse] = {}
```

This allows direct lookup with `self._tasks.get(task_id)`. My repository stored tasks in a list and searched through the list one task at a time.

The AI also explicitly returned a FastAPI `Response` for successful deletion:

```python
return Response(status_code=status.HTTP_204_NO_CONTENT)
```

This clearly guarantees that the `204 No Content` response has no response body.

I understand these changes well enough to explain how the response model, custom exceptions, dictionary storage, and explicit empty response work.

### What the AI Did Differently or Quietly Ignored

My hand-built API included filtering by completion status, title search, pagination, and a task statistics endpoint. The AI version did not include these features.

My version supports requests such as:

```text
GET /tasks?done=true
GET /tasks?search=gym
GET /tasks?limit=2&offset=2
GET /tasks/stats
```

The AI-generated `GET /tasks` endpoint only returns every stored task and does not accept query parameters.

My repository started with three example tasks, while the AI repository started with empty storage. This means `GET /tasks` produces different initial results in the two versions.

The AI created its `TaskRepository` inside the service:

```python
task_service = TaskService()
```

The service then created a repository when one was not provided. In my version, the router explicitly created the repository and passed it into the service:

```python
repository = TaskRepository()
service = TaskService(repository)
```

My approach makes the dependency injection more visible at the application setup level.

The AI used synchronous route functions with `def`, while my version used asynchronous route functions with `async def`. Both work for this small in-memory API, but the AI silently selected the synchronous approach.

### What My Prompt Forgot to Specify

My prompt did not mention the optional features I had added to my hand-built version: filtering, title search, pagination, and statistics. Because they were missing from the prompt, the AI generated only the five basic CRUD endpoints.

My prompt did not specify whether the in-memory repository should start empty or contain example tasks. The AI silently decided to start with an empty dictionary, while my version contained three initial tasks.

My prompt did not specify whether tasks should be stored as dictionaries, Pydantic objects, or another structure. The AI chose a dictionary of `TaskResponse` objects, while I used a list of dictionaries.

My prompt also did not specify whether route functions should use `def` or `async def`. The AI chose synchronous functions.

These differences show that details not included in the specification are left for the AI to decide.

### Improved Rematch Prompt

For the rematch, I would improve the prompt by adding the requirements that were missing:

```text
Build a second version of the Task Management REST API using Python and FastAPI.

Generate the project only inside ai-version/rematch. Do not modify files outside that folder.

Use the same layered architecture:

ai-version/rematch/
├── app/
│   ├── main.py
│   ├── routers/router.py
│   ├── services/service.py
│   ├── repositories/repository.py
│   └── schemas/schema.py
├── requirements.txt
└── README.md

Use in-memory storage only and do not use a database.

Use integer IDs and begin with these three example tasks:

1. Update to do list, done = true
2. Setup Flyrank profile, done = true
3. Go to the gym, done = false

Implement:

- GET /tasks
- GET /tasks/{task_id}
- POST /tasks
- PUT /tasks/{task_id}
- DELETE /tasks/{task_id}
- GET /tasks/stats
- GET /
- GET /health

GET /tasks must support:

- Filtering by completion status with the optional done Boolean query parameter
- Case-insensitive title search with the optional search query parameter
- Pagination with an optional limit parameter and an offset parameter
- limit must be at least 1 when supplied
- offset must be at least 0

GET /tasks/stats must return:

- total: total number of tasks
- done: completed task count
- open: incomplete task count

Validation requirements:

- Empty and whitespace-only titles must return HTTP 400
- PUT must allow title, done, or both
- PUT with no supplied fields must return HTTP 400
- Missing tasks must return HTTP 404
- POST must return HTTP 201
- DELETE must return HTTP 204 with no response body

Use:

- APIRouter with the /tasks prefix
- Pydantic request and response models
- FastAPI HTTPException and status constants
- Async endpoint functions
- Explicit dependency injection by constructing TaskRepository in router.py and passing it to TaskService
- Swagger summaries and descriptions
- FastAPI title, description, and version metadata

Keep HTTP handling in the router, business validation in the service, and in-memory data operations in the repository.

The application must run using:

uvicorn app.main:app --reload --port 8002
```

### Rematch Result

The improved prompt explicitly added filtering, case-insensitive title search, pagination, task statistics, initial task data, asynchronous routes, and repository dependency injection instead of allowing the AI to decide those details silently.