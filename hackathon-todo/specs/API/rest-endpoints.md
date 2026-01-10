# REST API Endpoints

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### Login (Form Data)
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password123

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Login (JSON)
```http
POST /auth/token
Content-Type: application/json

{
  "username": "username",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Task Endpoints (Protected)

All task endpoints require JWT authentication:
```http
Authorization: Bearer <access_token>
```

### List All Tasks
```http
GET /tasks
Query Parameters:
  - completed: boolean (optional)

Response: 200 OK
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the hackathon project",
    "completed": false,
    "owner_id": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Get Single Task
```http
GET /tasks/{id}

Response: 200 OK
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the hackathon project",
  "completed": false,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Create Task
```http
POST /tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "completed": false
}

Response: 201 Created
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Update Task
```http
PUT /tasks/{id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T01:00:00"
}
```

### Delete Task
```http
DELETE /tasks/{id}

Response: 204 No Content
```

### Mark Task Complete
```http
PATCH /tasks/{id}/complete

Response: 200 OK
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T01:00:00"
}
```

### Mark Task Incomplete
```http
PATCH /tasks/{id}/incomplete

Response: 200 OK
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T01:00:00"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this task"
}
```

### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## CORS Configuration

The API allows requests from:
- `http://localhost:3000`
- `http://localhost:3001`

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production deployment.

## Versioning

Current version: v1.0.0
No API versioning scheme implemented yet.
