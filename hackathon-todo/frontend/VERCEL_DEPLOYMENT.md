# Vercel Deployment Guide

## Prerequisites
- A Vercel account
- Your backend deployed and accessible (or use localhost for testing)

## Deployment Steps

### 1. Deploy to Vercel
You can deploy the frontend in two ways:

#### Option A: Deploy from GitHub
1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Import Project"
4. Select your GitHub repository
5. Set the root directory to `hackathon-todo/frontend`
6. Configure environment variables (see below)
7. Click "Deploy"

#### Option B: Deploy using Vercel CLI
```bash
cd hackathon-todo/frontend
npm install -g vercel
vercel login
vercel
```

### 2. Configure Environment Variables

In your Vercel project settings, add the following environment variable:

**Environment Variable:**
- `NEXT_PUBLIC_API_URL` - Your backend API URL

**Example values:**
- For production: `https://your-backend.vercel.app` or `https://your-backend-domain.com`
- For testing with local backend: `http://localhost:8000`

**How to add environment variables in Vercel:**
1. Go to your project dashboard on Vercel
2. Click on "Settings"
3. Click on "Environment Variables"
4. Add `NEXT_PUBLIC_API_URL` with your backend URL
5. Click "Save"
6. Redeploy your application

### 3. Redeploy After Configuration
After adding environment variables, you need to redeploy:
1. Go to "Deployments" tab
2. Click on the three dots (...) next to your latest deployment
3. Click "Redeploy"

## Troubleshooting

### 404 Error on Deployment
If you see a 404 error:
1. Check that the root directory is set to `hackathon-todo/frontend`
2. Verify that the build completed successfully
3. Check the build logs for any errors

### API Connection Issues
If the frontend deploys but can't connect to the backend:
1. Verify `NEXT_PUBLIC_API_URL` is set correctly
2. Make sure your backend allows CORS from your Vercel domain
3. Check that your backend is accessible from the internet

### Build Failures
If the build fails:
1. Check the build logs in Vercel dashboard
2. Make sure all dependencies are listed in `package.json`
3. Verify there are no TypeScript errors locally: `npm run build`

## Current Configuration

The frontend is configured with:
- Framework: Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

## Backend Setup

Don't forget to deploy your backend separately and update the `NEXT_PUBLIC_API_URL` environment variable with the backend URL.

Your backend should be accessible at a URL like:
- `https://your-backend.vercel.app` (if deployed on Vercel)
- `https://your-backend.herokuapp.com` (if deployed on Heroku)
- `https://api.yourdomain.com` (if using custom domain)

## Important Notes

1. **CORS Configuration**: Make sure your backend allows requests from your Vercel deployment domain
2. **Environment Variables**: `NEXT_PUBLIC_` prefix is required for client-side environment variables in Next.js
3. **API Routes**: All API calls are prefixed with `/auth` or `/api` as configured in the API client
