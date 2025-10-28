# Deployment Guide - Content Engine Web Interface

This guide covers deploying the Content Engine web interface to Vercel.

## Prerequisites

1. A Vercel account (https://vercel.com)
2. A PostgreSQL database (e.g., from Neon, Supabase, or Railway)
3. OpenRouter API key (https://openrouter.ai)

## Vercel Deployment Steps

### 1. Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your Git repository
4. Configure the project settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `web` (important!)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

### 2. Configure Environment Variables

In your Vercel project settings, go to **Settings > Environment Variables** and add:

#### Required Variables

- `DATABASE_URL`: Your PostgreSQL connection string
  - Example: `postgresql://user:password@host:5432/content_engine`
  - For production, use a service like [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app)

- `OPENROUTER_API_KEY`: Your OpenRouter API key
  - Example: `sk-or-v1-xxxxx...`
  - Get yours at https://openrouter.ai/keys

#### Optional Variables

- `API_SECRET_KEY`: Secret key for API authentication (if needed)
- `NEXT_PUBLIC_APP_URL`: Your production URL (e.g., `https://your-app.vercel.app`)

### 3. Deploy

After configuring environment variables:

1. Click "Deploy" or push to your main branch
2. Vercel will automatically build and deploy your application
3. Visit the generated URL to see your app live

## Important Limitations

### Job Execution Endpoint

The `/api/jobs/:id/execute` endpoint attempts to execute Python CLI commands, which **will not work** on Vercel's serverless environment by default, as it doesn't include a Python runtime.

**Options to resolve this:**

1. **Remove the execute endpoint** and run jobs manually via the Python CLI on your local machine
2. **Deploy a separate Python backend** on a service that supports Python (e.g., Railway, Render, Fly.io)
3. **Use Vercel's Python runtime** (experimental, requires additional configuration)
4. **Implement a job queue** (recommended for production):
   - Use a service like BullMQ, Inngest, or Trigger.dev
   - Queue jobs from the web interface
   - Process them with a separate worker service running Python

For now, the web interface can:
- ✅ Create and view jobs
- ✅ View job status and tasks
- ✅ Browse agents and templates
- ❌ Execute jobs (requires Python runtime)

## Database Setup

Make sure your PostgreSQL database has the required schema. You can initialize it by:

1. Running the Python CLI locally: `python cli.py init-db`
2. Or manually running the schema from `src/core/database.py`

## Vercel Configuration

The `vercel.json` file in this directory is minimal and relies on Vercel's automatic Next.js detection. Environment variables should be configured through the Vercel dashboard, not in the config file.

## Troubleshooting

### Build Failures

- Make sure the root directory is set to `web`
- Check that all dependencies are listed in `package.json`
- Review build logs in the Vercel dashboard

### Database Connection Issues

- Verify your `DATABASE_URL` is correct
- Ensure your database allows connections from Vercel's IP ranges
- Check that the database schema is initialized

### API Errors

- Check the Vercel Function logs under **Deployments > [Your Deployment] > Functions**
- Ensure environment variables are set for all environments (Production, Preview, Development)
- Verify your database is accessible and properly configured

## Local Development

To run locally:

```bash
cd web
npm install
cp .env.example .env
# Edit .env with your actual values
npm run dev
```

Visit http://localhost:3000

## Production Recommendations

For a production deployment, consider:

1. **Separate Python backend** deployed on Railway/Render
2. **Job queue system** for asynchronous job processing
3. **Redis cache** for better performance
4. **Monitoring** with Vercel Analytics or Sentry
5. **Database connection pooling** (e.g., PgBouncer)
6. **Rate limiting** for API routes
7. **Authentication** for sensitive endpoints

## Support

For issues specific to:
- **Vercel deployment**: Check [Vercel Docs](https://vercel.com/docs)
- **Content Engine**: See main project README
- **Database**: Consult your database provider's documentation
