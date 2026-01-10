# Task CRUD

## Overview
Complete CRUD (Create, Read, Update, Delete) operations for task management with JWT authentication.

## Features Implemented

### User Stories
- ✅ User can create tasks
- ✅ User can list all tasks
- ✅ User can filter tasks by completion status
- ✅ User can view a specific task
- ✅ User can update task title and description
- ✅ User can delete tasks
- ✅ User can mark tasks as complete/incomplete

### Task Model
Each task contains:
- `id`: Unique identifier (auto-generated)
- `title`: Task title (required, max 200 characters)
- `description`: Task description (optional)
- `completed`: Boolean completion status (default: false)
- `owner_id`: User who owns the task (foreign key)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### API Endpoints

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

#### List Tasks
```
GET /tasks
Query Parameters:
  - completed (optional): boolean to filter by status
```

#### Get Task
```
GET /tasks/{id}
```

#### Create Task
```
POST /tasks
Body:
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": boolean (optional, default: false)
}
```

#### Update Task
```
PUT /tasks/{id}
Body:
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": boolean (optional)
}
```

#### Delete Task
```
DELETE /tasks/{id}
```

#### Mark Complete
```
PATCH /tasks/{id}/complete
```

#### Mark Incomplete
```
PATCH /tasks/{id}/incomplete
```

## Security
- All endpoints require valid JWT token
- Users can only access their own tasks
- Ownership verification on all operations
- Returns 403 Forbidden for unauthorized access

## Frontend Implementation
- Task list page with filters (All/Active/Completed)
- Add task form
- Inline editing
- Delete confirmation
- Toggle completion with checkbox
- Real-time updates after operations

## Technical Implementation
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT Bearer tokens
- **Validation**: Pydantic models
- **Frontend**: Next.js with TypeScript
