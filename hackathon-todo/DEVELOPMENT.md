# Development Guide

## Project Overview

Full-stack task management application with:
- **Backend**: FastAPI + SQLModel + PostgreSQL
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT tokens

## Development Workflow

### Backend Development

#### Adding a New Endpoint

1. **Create the route** in `app/routers/`:
```python
@router.get("/tasks/stats")
async def get_task_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    total = len(current_user.tasks)
    completed = len([t for t in current_user.tasks if t.completed])
    return {"total": total, "completed": completed}
```

2. **Register the router** in `app/main.py` (if new file):
```python
from app.routers import auth, tasks, stats

app.include_router(stats.router)
```

3. **Test** at `http://localhost:8000/docs`

#### Adding a Database Model

1. **Define the model** in `app/models.py`:
```python
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id")
```

2. **Add relationships** if needed:
```python
class Task(TaskBase, table=True):
    category_id: Optional[int] = Field(foreign_key="category.id")
    category: Optional[Category] = Relationship()
```

3. **Restart the server** - tables auto-create on startup

#### Database Migrations

For production, use Alembic:
```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Add categories"
alembic upgrade head
```

### Frontend Development

#### Adding a New Page

1. **Create page** in `frontend/src/app/`:
```typescript
// app/settings/page.tsx
"use client";

export default function SettingsPage() {
  return <div>Settings</div>;
}
```

2. **Add navigation** in your layout/components

#### Creating a Component

1. **Create component** in `frontend/src/components/`:
```typescript
// components/TaskCard.tsx
import { Task } from '@/lib/api';

export function TaskCard({ task }: { task: Task }) {
  return (
    <div className="border rounded p-4">
      <h3>{task.title}</h3>
    </div>
  );
}
```

2. **Use in page**:
```typescript
import { TaskCard } from '@/components/TaskCard';
```

#### Adding an API Call

1. **Update** `frontend/src/lib/api.ts`:
```typescript
export const tasksAPI = {
  // ... existing methods

  getStats: async () => {
    const response = await api.get<{ total: number, completed: number }>('/tasks/stats');
    return response.data;
  },
};
```

2. **Use in component**:
```typescript
const [stats, setStats] = useState(null);

useEffect(() => {
  tasksAPI.getStats().then(setStats);
}, []);
```

## Code Style

### Backend (Python)

Follow PEP 8:
```python
# Good
def get_user_tasks(user_id: int, completed: bool = None) -> list[Task]:
    """Get tasks for a user."""
    pass

# Use type hints
# Use docstrings
# 4-space indentation
```

### Frontend (TypeScript)

```typescript
// Use TypeScript types
interface TaskProps {
  task: Task;
  onUpdate: (task: Task) => void;
}

// Use async/await
const loadTasks = async () => {
  const data = await tasksAPI.list();
  setTasks(data);
};

// Use descriptive names
const [isLoading, setIsLoading] = useState(false);
```

## Testing

### Backend Tests

Create `tests/test_tasks.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    # Get auth token first
    response = client.post("/auth/token", json={
        "username": "test",
        "password": "test"
    })
    token = response.json()["access_token"]

    # Create task
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test task"}
    )
    assert response.status_code == 201
```

Run tests:
```bash
pytest
```

### Frontend Tests

Add Jest and React Testing Library:
```bash
npm install -D jest @testing-library/react @testing-library/jest-dom
```

Create `__tests__/TaskCard.test.tsx`:
```typescript
import { render, screen } from '@testing-library/react';
import { TaskCard } from '@/components/TaskCard';

test('renders task title', () => {
  const task = { id: 1, title: 'Test', completed: false };
  render(<TaskCard task={task} />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

## Environment Setup

### Backend .env
```env
# Database
DATABASE_URL=postgresql://user:pass@host/db

# JWT
SECRET_KEY=min-32-chars-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=True
```

### Frontend .env.local
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Common Issues

### CORS Errors
Add allowed origin in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Connection Issues
- Check DATABASE_URL format
- Verify database is accessible
- Check SSL settings for Neon

### Token Expiration
Tokens expire after 30 minutes. Implement refresh tokens or increase expiration.

## Deployment

### Backend (Railway)
1. Connect GitHub repo
2. Add environment variables
3. Deploy automatically on push

### Frontend (Vercel)
1. Import GitHub repo
2. Set NEXT_PUBLIC_API_URL
3. Deploy automatically on push

### Database (Neon)
- Already serverless
- Auto-scales
- Just use the connection string

## Useful Commands

### Backend
```bash
# Format code
black app/

# Type checking
mypy app/

# Lint
flake8 app/

# Run server
uvicorn app.main:app --reload

# Shell into database
psql $DATABASE_URL
```

### Frontend
```bash
# Format code
npm run format

# Type check
npm run type-check

# Lint
npm run lint

# Build
npm run build

# Analyze bundle
npm run analyze
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/task-categories

# Make changes and commit
git add .
git commit -m "Add task categories feature"

# Push and create PR
git push origin feature/task-categories
```

## Architecture Decisions

### Why FastAPI?
- Auto-generated API docs
- Async support
- Type safety with Pydantic
- Fast performance

### Why SQLModel?
- Combines SQLAlchemy + Pydantic
- Type-safe database operations
- Easy migrations

### Why Next.js?
- Server-side rendering
- File-based routing
- Built-in optimizations
- Great developer experience

### Why JWT?
- Stateless authentication
- Works across services
- Easy to implement
- Industry standard

## Performance Tips

### Backend
- Use connection pooling
- Add database indexes
- Cache frequent queries
- Use async endpoints

### Frontend
- Lazy load components
- Optimize images
- Use React.memo for expensive components
- Implement pagination

## Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens signed
- [x] HTTPS in production
- [x] CORS configured
- [x] SQL injection prevented (SQLModel)
- [x] XSS prevented (React escapes by default)
- [ ] Rate limiting (TODO)
- [ ] Input validation on all endpoints
- [ ] Security headers (TODO)

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Neon Docs](https://neon.tech/docs)
- [Tailwind CSS](https://tailwindcss.com/)
