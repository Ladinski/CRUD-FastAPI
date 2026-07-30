# Task Management API

A layered FastAPI REST API for managing tasks with in-memory storage.

## Project Structure

```text
app/
├── main.py
├── routers/
│   └── router.py
├── services/
│   └── service.py
├── repositories/
│   └── repository.py
└── schemas/
    └── schema.py
```

## Requirements

- Python 3.10 or newer
- FastAPI
- Uvicorn

## Installation

From inside the `ai-version` folder, create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the API from inside the `ai-version` folder:

```bash
uvicorn app.main:app --reload --port 8001
```

Swagger UI is available at:

```text
http://127.0.0.1:8001/docs
```

## Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /tasks` - Return all tasks
- `GET /tasks/{task_id}` - Return one task by ID
- `POST /tasks` - Create a task
- `PUT /tasks/{task_id}` - Partially update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Example Task Payloads

Create a task:

```json
{
  "title": "Write project README"
}
```

Update a task:

```json
{
  "title": "Write final README",
  "done": true
}
```
