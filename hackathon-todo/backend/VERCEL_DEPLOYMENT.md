# Backend Vercel Deployment Guide

## Overview
This guide will help you deploy the FastAPI backend to Vercel. The backend supports **FREE demo mode** - no API key required!

## Features
- FastAPI REST API
- Task management endpoints
- AI Chat agent (with demo mode)
- CORS enabled for frontend integration

## Quick Start - FREE Demo Mode

The backend has a **FREE demo mode** that works without any API keys! Just set:
```
OPENAI_API_KEY=demo
```

In demo mode, the AI agent uses simple pattern matching to understand commands without calling OpenAI API.

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare backend for Vercel deployment"
   git push
   ```

2. **Go to Vercel Dashboard**
   - Visit [https://vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your GitHub repository

3. **Configure Project**
   - **Root Directory**: Set to `hackathon-todo/backend`
   - **Framework Preset**: Other
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. **Add Environment Variables**
   Click "Environment Variables" and add:

   **For FREE Demo Mode (No API Key Required):**
   - Key: `OPENAI_API_KEY`
   - Value: `demo`

   **OR for Full OpenAI Features:**
   - Key: `OPENAI_API_KEY`
   - Value: Your actual OpenAI API key (starts with sk-...)

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Copy your deployment URL (e.g., `https://your-backend.vercel.app`)

### Method 2: Deploy via Vercel CLI

```bash
cd hackathon-todo/backend

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? hackathon-todo-backend
# - Directory? ./
# - Override settings? No

# For production deployment
vercel --prod
```

## Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Value | Required |
|----------|-------|----------|
| `OPENAI_API_KEY` | `demo` or your OpenAI key | Yes (use "demo" for free mode) |

### Using Demo Mode (FREE - No API Key)

Set `OPENAI_API_KEY=demo` in Vercel environment variables. The agent will:
- Use pattern matching to understand commands
- Support Hindi/Hinglish commands
- Work completely FREE without any API calls!

Supported demo commands:
- "Add a task to buy groceries"
- "Show me my tasks"
- "Complete task ID: xyz"
- "Delete the first task"
- "Kal ka kaam add kar do" (Hindi/Hinglish)

## API Endpoints

After deployment, your backend will have these endpoints:

### Task Management
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Mark task as complete

### AI Chat
- `POST /api/chat` - Chat with AI agent
- `GET /chat/conversations` - List conversations
- `GET /chat/conversations/{id}` - Get specific conversation
- `DELETE /chat/conversations/{id}` - Delete conversation

### Authentication (Stub for Phase 3)
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get token

### Root
- `GET /` - API info and available endpoints

## Testing Your Deployment

After deployment, test with curl:

```bash
# Replace YOUR_BACKEND_URL with your actual Vercel URL
export BACKEND_URL="https://your-backend.vercel.app"

# Test root endpoint
curl $BACKEND_URL/

# Create a task
curl -X POST $BACKEND_URL/api/tasks \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Test Task", "description": "Testing Vercel deployment"}'

# List tasks
curl $BACKEND_URL/api/tasks

# Chat with AI (demo mode)
curl -X POST $BACKEND_URL/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Add a task to buy groceries"}'
```

## Update Frontend with Backend URL

After deploying the backend, update your frontend's environment variable:

1. Go to your frontend project on Vercel
2. Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` with your backend URL
4. Redeploy the frontend

## Important Notes

### Storage Limitations
⚠️ **Vercel's serverless functions are stateless**:
- File storage (tasks.json) won't persist between requests
- SQLite database (conversations.db) won't persist between requests

**For production use**, you should:
- Use a cloud database (PostgreSQL on Vercel, Supabase, PlanetScale, etc.)
- Use cloud storage for files (S3, Vercel Blob, etc.)

**For demo/testing**, the current implementation will work but data won't persist.

### CORS Configuration
The backend is configured with:
```python
allow_origins=["*"]  # Allows all origins
```

For production, update this in `main.py` to only allow your frontend domain:
```python
allow_origins=["https://your-frontend.vercel.app"]
```

## Troubleshooting

### Build Fails
1. Check build logs in Vercel dashboard
2. Verify requirements.txt is in the backend folder
3. Make sure all imports are available

### 500 Internal Server Error
1. Check Function Logs in Vercel dashboard
2. Verify environment variables are set
3. Check for file path issues (use absolute paths)

### CORS Errors
1. Verify CORS middleware is configured
2. Check allowed origins in main.py
3. Make sure preflight OPTIONS requests are handled

### Demo Mode Not Working
1. Verify `OPENAI_API_KEY` is set to `demo`
2. Check Function Logs for errors
3. Try simple commands first: "Show me my tasks"

## Cost Considerations

### FREE Demo Mode
- Zero API costs
- Uses pattern matching only
- Perfect for testing and development
- Supports English and Hindi/Hinglish

### OpenAI Mode
- Costs depend on usage
- Uses GPT-4o-mini model
- More intelligent responses
- Better natural language understanding

## Next Steps

1. Deploy the backend following the steps above
2. Copy your backend URL
3. Update frontend `NEXT_PUBLIC_API_URL` with backend URL
4. Redeploy frontend
5. Test the complete application!

## Support

If you encounter issues:
1. Check Vercel Function Logs
2. Verify environment variables
3. Test endpoints individually with curl
4. Check CORS configuration

Happy deploying! 🚀
