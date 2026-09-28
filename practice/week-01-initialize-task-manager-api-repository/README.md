# Task Manager REST API

A production-ready, modular Task Manager REST API built with **FastAPI**, **Pydantic v2**, and **Uvicorn**, implementing industry-validated architectural patterns, schema validation, and complete automated test coverage.

---

## Overview

The **Task Manager REST API** provides a robust backend foundation for managing project tasks throughout their lifecycle. Designed using a clean layered architecture, the API separates routing concerns, business logic, and domain schemas to achieve high maintainability, thread safety, and extensibility.

### Key Features

- **Standard RESTful Endpoints**: Full CRUD capabilities for task resources (`POST`, `GET`, `PUT`, `DELETE`).
- **Validated Schemas**: Strict request parsing and response modeling using Pydantic v2.
- **Workflow State Management**: Support for task lifecycle transitions (`Pending`, `In Progress`, `Completed`).
- **Query & Filtering**: Filter tasks by status and search tasks by keywords across title and description.
- **Health Checks & Observability**: Dedicated `/health` and `/api/v1/health` status endpoints.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`) powered by OpenAPI 3.1.
- **Automated Test Suite**: Comprehensive integration and unit tests using `pytest` and `fastapi.testclient.TestClient`.

---

## Architecture & Validated Patterns

The project follows a clean **Layered Architecture** adhering to the Separation of Concerns (SoC) principle:

```
[ Client Request ]
        │
        ▼
[ API Routing Layer ]       ──> src/api/ (endpoints, HTTP status codes, query validation)
        │
        ▼
[ Service / Logic Layer ]   ──> src/services/ (task business logic, thread-safe persistence)
        │
        ▼
[ Domain & Model Layer ]    ──> src/models/ (Pydantic schemas, enums, data contracts)
        │
[ Configuration Layer ]     ──> config/ (environment variables, application settings)
```

1. **Presentation Layer (`src/api/`)**: Defines routers, handles HTTP serialization, parameter validation, and status code dispatching.
2. **Service Layer (`src/services/`)**: Encapsulates business rules and data access within a thread-safe singleton service (`TaskService`).
3. **Domain Layer (`src/models/`)**: Declares typed schemas (`TaskCreate`, `TaskUpdate`, `TaskResponse`) and enumerations (`TaskStatus`).
4. **Configuration (`config/`)**: Centralizes application settings (`Settings`), allowing environment-driven configuration for host, port, CORS, and debugging.

---

## Project Structure

```
task-manager-api/
├── config/
│   ├── __init__.py          # Config package exports
│   └── settings.py          # Application settings & environment configuration
├── src/
│   ├── __init__.py          # Source package marker
│   ├── api/
│   │   ├── __init__.py      # Router exports
│   │   ├── health.py        # Health check endpoint (/health)
│   │   └── routes.py        # Task CRUD REST endpoints (/api/v1/tasks)
│   ├── models/
│   │   ├── __init__.py      # Model exports
│   │   └── task.py          # Pydantic models (TaskCreate, TaskUpdate, TaskResponse, TaskStatus)
│   ├── services/
│   │   ├── __init__.py      # Service exports
│   │   └── task_service.py  # Thread-safe in-memory task service
│   └── main.py              # FastAPI application factory and middleware configuration
├── tests/
│   ├── __init__.py          # Test package marker
│   ├── test_health.py       # Health check and root endpoint tests
│   └── test_tasks.py        # Complete Task CRUD, validation, and filter tests
├── .gitignore               # Python and environment exclusion rules
├── main.py                  # Root entrypoint to run the server
├── README.md                # Project documentation and setup guide
└── requirements.txt         # Production and development dependencies
```

---

## Getting Started

### Prerequisites

- **Python**: Version 3.10+ (tested on Python 3.11)
- **pip**: Python package manager
- **git**: Distributed version control

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/parth-mehta95/task-manager-api.git
   cd task-manager-api
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # On Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Option 1: Run via Python Entrypoint
```bash
python main.py
```

### Option 2: Run via Uvicorn CLI
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once started, the API is available at:
- **API Base**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

---

## API Endpoints Reference

| HTTP Method | Endpoint | Description | Request Body | Success Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API welcome and links | None | `200 OK` |
| `GET` | `/health` | Service health status | None | `200 OK` |
| `GET` | `/api/v1/health` | Versioned health status | None | `200 OK` |
| `POST` | `/api/v1/tasks` | Create a new task | `TaskCreate` | `201 Created` |
| `GET` | `/api/v1/tasks` | List all tasks (optional filter) | None | `200 OK` |
| `GET` | `/api/v1/tasks/{id}` | Get task by ID | None | `200 OK` |
| `PUT` | `/api/v1/tasks/{id}` | Update task details | `TaskUpdate` | `200 OK` |
| `DELETE` | `/api/v1/tasks/{id}` | Delete task by ID | None | `204 No Content` |

### Task Status Enum
- `Pending` (Default)
- `In Progress`
- `Completed`

---

## Example Usage with cURL

### 1. Check Service Health
```bash
curl -X GET http://localhost:8000/health
```

### 2. Create a Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build authentication module",
    "description": "Implement JWT-based bearer authentication and refresh tokens",
    "status": "Pending"
  }'
```

### 3. List All Tasks
```bash
curl -X GET http://localhost:8000/api/v1/tasks
```

### 4. Filter Tasks by Status
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=Pending"
```

### 5. Search Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?search=authentication"
```

### 6. Get Task by ID
```bash
curl -X GET http://localhost:8000/api/v1/tasks/1
```

### 7. Update Task
```bash
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }'
```

### 8. Delete Task
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1
```

---

## Running Automated Tests

The test suite validates status codes, payload contracts, validation constraints, and error scenarios:

```bash
python -m pytest -v
```

To run with coverage (optional):
```bash
python -m pytest --cov=src --cov-report=term-missing
```

---

## License

This project is licensed under the MIT License.