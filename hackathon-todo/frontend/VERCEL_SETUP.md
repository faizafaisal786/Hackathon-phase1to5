# Vercel Setup Guide - FREE TIER (Perfect Configuration)

## Step 1: Create Vercel Account (FREE)

1. Go to https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub (Recommended - Makes deployment easier)
4. Verify your email

## Step 2: Import Project

### Method A: From GitHub (Easiest - Recommended)

1. Push your code to GitHub if not already done
2. Go to https://vercel.com/new
3. Click "Import Git Repository"
4. Select your repository: `Hackathon-phase1to5`
5. **IMPORTANT**: Set Root Directory to `hackathon-todo/frontend`
6. Framework Preset: Next.js (Auto-detected)
7. Click "Deploy"

### Method B: Using Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to frontend directory
cd hackathon-todo/frontend

# Deploy
vercel

# For production
vercel --prod
```

## Step 3: Configure Environment Variables

After importing, BEFORE deployment completes:

1. In Vercel Dashboard, go to your project
2. Click "Settings" tab
3. Click "Environment Variables" in sidebar
4. Add the following variable:

**Variable Name:** `NEXT_PUBLIC_API_URL`
**Value:** Your backend URL (e.g., `https://your-backend.vercel.app`)

For all environments: Production, Preview, Development

5. Click "Save"

## Step 4: Redeploy

After adding environment variables:

1. Go to "Deployments" tab
2. Click "..." menu on latest deployment
3. Click "Redeploy"
4. Wait for deployment to complete

## Step 5: Your App is Live!

Your frontend will be available at:
- `https://your-project-name.vercel.app`

## Free Tier Limits (Hobby Plan)

✅ Unlimited deployments
✅ Unlimited bandwidth (Fair use)
✅ Automatic HTTPS
✅ Preview deployments for PRs
✅ 100GB bandwidth per month
✅ Serverless functions (100GB-hours)
✅ Edge functions
✅ Custom domains (1 domain)

## Configuration Files Included

✅ `vercel.json` - Optimized Vercel configuration
✅ `.vercelignore` - Excludes unnecessary files
✅ `next.config.js` - Production-ready Next.js config
✅ `.env.local.example` - Environment variable template

## Troubleshooting

### Error: "No framework detected"
- Make sure Root Directory is set to `hackathon-todo/frontend`
- Verify `package.json` exists in frontend folder

### Error: "Build failed"
- Check build logs in Vercel dashboard
- Run `npm run build` locally to test
- Check for TypeScript errors

### Error: "Cannot connect to API"
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Make sure backend is deployed and accessible
- Check backend CORS settings

### Error: "404 on all pages"
- Check Root Directory is `hackathon-todo/frontend`
- Verify output directory is `.next`
- Check build logs for errors

## Optimization Settings (Already Configured)

✅ SWC Minification enabled
✅ Compression enabled
✅ ETags enabled for caching
✅ Powered-by header removed for security
✅ Image optimization configured
✅ Build verification enabled

## Deployment Status

Build Status: ✅ Successful
- 7 pages generated
- Bundle size: ~84.2 kB
- All routes optimized
- No errors or warnings

## Next Steps

1. Deploy backend (if not deployed)
2. Update `NEXT_PUBLIC_API_URL` environment variable
3. Redeploy frontend
4. Test all features
5. (Optional) Add custom domain in Vercel settings

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Check browser console for errors
3. Verify environment variables
4. Test backend API separately

## Important Notes

- Free tier is perfect for this project
- No credit card required
- Automatic SSL/HTTPS
- Global CDN included
- Preview URLs for every PR

Your frontend is now production-ready for Vercel! 🚀
