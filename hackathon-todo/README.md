# Hackathon Todo

A modern full-stack task management application built with **FastAPI**, **Next.js**, **SQLModel**, and **Neon PostgreSQL**.

## Features

- **User Authentication**: JWT-based secure authentication
- **Task CRUD Operations**: Create, Read, Update, Delete tasks
- **Task Management**: Mark tasks as complete/incomplete, filter by status
- **Protected Routes**: All task operations require authentication
- **Modern UI**: Responsive design with Tailwind CSS
- **Type Safety**: TypeScript frontend and Python type hints in backend

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLModel**: SQL database ORM with Pydantic integration
- **Neon PostgreSQL**: Serverless PostgreSQL database
- **JWT Authentication**: Secure token-based authentication
- **Python 3.10+**

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API requests

## Project Structure

```
hackathon-todo/
├── app/                    # FastAPI backend
│   ├── routers/
│   │   ├── auth.py        # Authentication endpoints
│   │   └── tasks.py       # Task CRUD endpoints
│   ├── models.py          # SQLModel database models
│   ├── auth.py            # JWT utilities
│   ├── database.py        # Database connection
│   ├── dependencies.py    # FastAPI dependencies
│   ├── config.py          # Configuration settings
│   └── main.py            # Main FastAPI app
├── frontend/              # Next.js frontend
│   └── src/
│       ├── app/           # Next.js pages
│       ├── components/    # React components
│       ├── contexts/      # React contexts (Auth)
│       └── lib/           # API client
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Neon PostgreSQL database (or any PostgreSQL instance)

### Backend Setup

1. **Navigate to the project root**:
   ```bash
   cd hackathon-todo
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Neon database URL:
   ```env
   DATABASE_URL=postgresql://user:password@host/database
   SECRET_KEY=your-secret-key-here-change-this
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   APP_NAME=Hackathon Todo API
   DEBUG=True
   ```

5. **Run the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env.local` file:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password",
    "full_name": "Full Name"
  }
  ```

- `POST /auth/login` - Login (form data)
- `POST /auth/token` - Login (JSON)
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

### Tasks (All require JWT authentication)

- `GET /tasks` - List all tasks (optional `?completed=true/false`)
- `POST /tasks` - Create a new task
  ```json
  {
    "title": "Task title",
    "description": "Task description",
    "completed": false
  }
  ```
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/complete` - Mark task as complete
- `PATCH /tasks/{id}/incomplete` - Mark task as incomplete

## Authentication Flow

1. User registers or logs in via `/auth/register` or `/auth/token`
2. Backend returns a JWT access token
3. Frontend stores the token in localStorage
4. Token is included in all subsequent API requests via `Authorization: Bearer <token>` header
5. Backend validates the token on protected routes

## Database Schema

### User Table
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `full_name` (Optional)
- `hashed_password`
- `is_active`
- `created_at`

### Task Table
- `id` (Primary Key)
- `title`
- `description` (Optional)
- `completed` (Boolean)
- `owner_id` (Foreign Key to User)
- `created_at`
- `updated_at`

## Development

### Running Tests
```bash
# Backend tests (add pytest configuration)
pytest

# Frontend tests (add test framework)
npm test
```

### Building for Production

**Backend**:
```bash
# The FastAPI app can be deployed to any platform supporting Python
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
npm start
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT encoding
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `DEBUG`: Debug mode (True/False)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected API routes
- CORS configuration for frontend
- User ownership verification for tasks

## Deployment

### Backend Deployment Options
- **Railway**: Easy deployment with PostgreSQL
- **Render**: Free tier available
- **Heroku**: Classic PaaS option
- **DigitalOcean App Platform**: Managed deployment

### Frontend Deployment Options
- **Vercel**: Optimized for Next.js
- **Netlify**: Static site hosting
- **Railway**: Full-stack deployment

### Neon Database
The app is configured to work with Neon's serverless PostgreSQL. Get your connection string from [neon.tech](https://neon.tech).

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues and questions, please open an issue on the GitHub repository.
