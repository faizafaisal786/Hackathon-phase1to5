# Quick Start Guide

Get the Hackathon Todo app running in 5 minutes!

## Prerequisites

Make sure you have installed:
- Python 3.10+
- Node.js 18+
- A Neon PostgreSQL database (or any PostgreSQL instance)

## Step 1: Clone and Setup

```bash
cd hackathon-todo
```

## Step 2: Backend Setup (2 minutes)

### Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Configure Environment
```bash
# Copy example env file
cp .env.example .env
```

Edit `.env` and add your Neon database URL:
```env
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=change-this-to-a-random-string-min-32-chars
```

**Get your Neon database URL:**
1. Go to [neon.tech](https://neon.tech)
2. Create a free account
3. Create a new project
4. Copy the connection string from the dashboard

### Run Backend
```bash
uvicorn app.main:app --reload
```

Backend is now running at `http://localhost:8000`

Check it out: `http://localhost:8000/docs` 🎉

## Step 3: Frontend Setup (2 minutes)

Open a new terminal:

```bash
cd frontend
npm install
```

### Configure Frontend Environment
```bash
cp .env.local.example .env.local
```

The default settings should work:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Frontend
```bash
npm run dev
```

Frontend is now running at `http://localhost:3000`

## Step 4: Try It Out!

1. Open `http://localhost:3000`
2. Click "Register" to create an account
3. Fill in your details and register
4. You'll be redirected to the tasks page
5. Create your first task!

## What's Next?

### Explore the API
Visit `http://localhost:8000/docs` to see all available endpoints and try them out interactively.

### Customize
- Update the app name in `app/config.py`
- Change the color scheme in `frontend/tailwind.config.js`
- Add new features!

## Troubleshooting

### Backend won't start
- Check your DATABASE_URL is correct
- Make sure PostgreSQL is accessible
- Verify Python version: `python --version` (should be 3.10+)

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Try deleting `node_modules` and running `npm install` again
- Make sure backend is running on port 8000

### Can't connect to database
- Verify your Neon database is active
- Check the connection string format
- Ensure your IP is allowed (Neon allows all by default)

### CORS errors
- Make sure backend is running on `http://localhost:8000`
- Check that frontend URL is allowed in `app/main.py` CORS config

## Environment Variables Reference

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Common Commands

### Backend
```bash
# Run server
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --port 8001

# Production mode (no reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint
npm run lint
```

## Project Structure

```
hackathon-todo/
├── app/               # FastAPI backend
│   ├── routers/      # API routes
│   ├── models.py     # Database models
│   ├── auth.py       # JWT utilities
│   └── main.py       # App entry point
├── frontend/         # Next.js frontend
│   └── src/
│       ├── app/      # Pages
│       ├── contexts/ # React contexts
│       └── lib/      # API client
└── requirements.txt  # Python deps
```

## Need Help?

- Check the full README.md for detailed documentation
- Review API docs at `/docs`
- Open an issue on GitHub

Happy coding! 🚀
