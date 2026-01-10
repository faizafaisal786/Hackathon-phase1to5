# Database Schema

## Overview
PostgreSQL database schema using SQLModel ORM.

## Database Provider
**Neon PostgreSQL** - Serverless PostgreSQL with autoscaling

## Tables

### User Table
Stores user account information.

```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_username ON user(username);
```

**Fields:**
- `id` (integer, primary key): Auto-incrementing user ID
- `email` (string, unique): User's email address
- `username` (string, unique): Unique username
- `full_name` (string, nullable): User's full name
- `hashed_password` (string): Bcrypt-hashed password
- `is_active` (boolean): Account status flag
- `created_at` (timestamp): Account creation timestamp

### Task Table
Stores tasks owned by users.

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_owner_id ON task(owner_id);
CREATE INDEX idx_task_completed ON task(completed);
```

**Fields:**
- `id` (integer, primary key): Auto-incrementing task ID
- `title` (string, max 200): Task title
- `description` (text, nullable): Detailed task description
- `completed` (boolean): Completion status
- `owner_id` (integer, foreign key): References user.id
- `created_at` (timestamp): Task creation timestamp
- `updated_at` (timestamp): Last modification timestamp

## Relationships

### One-to-Many: User → Tasks
- One user can have many tasks
- Each task belongs to exactly one user
- Cascade delete: Deleting a user deletes all their tasks

```python
# SQLModel Relationship
class User(SQLModel, table=True):
    tasks: list["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    owner: Optional[User] = Relationship(back_populates="tasks")
```

## Indexes
- `idx_user_email`: Fast lookup by email
- `idx_user_username`: Fast lookup by username
- `idx_task_owner_id`: Fast filtering tasks by owner
- `idx_task_completed`: Fast filtering by completion status

## Constraints
- Email must be unique
- Username must be unique
- Task must have an owner (owner_id NOT NULL)
- Cascading delete on user removal

## Data Types
- **VARCHAR**: Limited-length strings (email, username, title)
- **TEXT**: Unlimited text (description)
- **BOOLEAN**: True/false flags (is_active, completed)
- **INTEGER**: Numeric IDs
- **TIMESTAMP**: Date and time information

## Security Considerations
- Passwords are never stored in plain text
- Bcrypt hashing algorithm used for password security
- User ownership enforced at application level
- No direct database access from frontend

## Migration Strategy
Tables are automatically created via SQLModel's `create_all()` on application startup.

For production:
```python
# In app/main.py lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
```

## Connection String Format
```
postgresql://user:password@host:port/database
```

For Neon:
```
postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

## Connection Pooling
SQLModel uses SQLAlchemy's default connection pooling:
- Pool size: 5 connections (default)
- Max overflow: 10 connections (default)
- Pool pre-ping enabled for health checks

## Future Enhancements
- Add task categories/tags table
- Add task priority field
- Add task due dates
- Add task sharing/collaboration
- Add activity/audit log table
- Add user profile pictures table
