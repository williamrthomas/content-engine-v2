# Content Engine V2 - Web Interface

Professional web interface for Content Engine V2, built with Next.js and deployed on Vercel.

## 🚀 Quick Start

### Local Development

```bash
# 1. Install dependencies
cd web
npm install

# 2. Configure environment
cp .env.example .env.local
# Edit .env.local with your DATABASE_URL

# 3. Run development server
npm run dev

# Open http://localhost:3000
```

### Vercel Deployment

#### Option 1: Vercel CLI (Recommended)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy from web directory
cd web
vercel

# Follow the prompts:
# - Set up new project
# - Link to Git (optional)
# - Configure environment variables when prompted
```

#### Option 2: GitHub Integration

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add web interface"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/new
   - Import your repository
   - Select the `web` directory as the root
   - Configure environment variables:
     - `DATABASE_URL`: Your PostgreSQL connection string

3. **Deploy**
   - Vercel will automatically build and deploy
   - Get your production URL: `https://your-project.vercel.app`

## 🔧 Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

```bash
# Required
DATABASE_URL=postgresql://user:password@host:5432/content_engine

# Optional
API_SECRET_KEY=your-secret-key
NEXT_PUBLIC_APP_URL=https://your-domain.vercel.app
```

## 📋 Features

### ✅ Implemented

- **Dashboard**: Overview of jobs, stats, and quick navigation
- **Job Management**: Create, view, list, and execute jobs
- **Real-time Updates**: Auto-refresh job status every 5 seconds
- **Template Selection**: Browse and select templates or use LLM auto-selection
- **Task Tracking**: View detailed task progress and results
- **Database Integration**: Direct connection to PostgreSQL (shared with CLI)

### 🎯 Pages

| Page | Route | Description |
|------|-------|-------------|
| Dashboard | `/` | Overview with stats and recent jobs |
| Job List | `/jobs` | All jobs with filtering |
| Job Detail | `/jobs/:id` | Detailed job view with tasks |
| Create Job | `/jobs/new` | Form to create new jobs |

### 🔌 API Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs` | GET | List all jobs |
| `/api/jobs` | POST | Create new job |
| `/api/jobs/:id` | GET | Get job details with tasks |
| `/api/jobs/:id/execute` | POST | Trigger job execution |
| `/api/templates` | GET | List available templates |
| `/api/agents` | GET | List registered agents |

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│         Vercel Deployment                │
│  ┌────────────────────────────────────┐  │
│  │  Next.js Frontend (React + TS)    │  │
│  │  - Dashboard, Jobs, Templates     │  │
│  │  - Real-time updates (SWR)        │  │
│  │  - Tailwind CSS styling           │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  API Routes (Serverless)          │  │
│  │  - Node.js serverless functions   │  │
│  │  - Direct PostgreSQL access       │  │
│  │  - Job execution triggers          │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────┐
│    Shared PostgreSQL Database            │
│    (Accessible by both Web & CLI)        │
└──────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────┐
│    Content Engine CLI (Python)           │
│    - Job execution                       │
│    - Agent orchestration                 │
│    - LLM & Freepik integration          │
└──────────────────────────────────────────┘
```

## 🔄 How It Works

### Creating Jobs

1. User fills form at `/jobs/new`
2. Frontend calls `POST /api/jobs`
3. API creates job record in PostgreSQL
4. Job status: `pending`

### Executing Jobs

1. User clicks "Execute" on job detail page
2. Frontend calls `POST /api/jobs/:id/execute`
3. API spawns Python CLI process: `python cli.py run <job-id>`
4. CLI processes job asynchronously
5. Frontend polls job status every 3 seconds
6. User sees real-time progress updates

### Database Sharing

The web interface connects to the **same PostgreSQL database** as the CLI:

```
Web (Node.js) ──┐
                ├──> PostgreSQL Database
CLI (Python) ───┘
```

This enables:
- ✅ Create jobs in web, execute in CLI
- ✅ View CLI-created jobs in web
- ✅ Real-time status updates
- ✅ Full job history access

## 📦 Stack

| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework with API routes |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **SWR** | Data fetching with caching |
| **pg** | PostgreSQL client for Node.js |
| **Vercel** | Hosting and serverless functions |

## 🚀 Production Considerations

### Database Connection Pooling

The app uses connection pooling for PostgreSQL:

```typescript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,              // Maximum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Job Execution

Currently uses `child_process.exec()` to spawn CLI. For production:

**Recommended Improvements:**
1. **Job Queue**: Use BullMQ, Celery, or SQS
2. **Worker Processes**: Dedicated workers for job execution
3. **Webhooks**: CLI posts results back to API
4. **Serverless Functions**: Move execution to serverless workers

### Scaling

- **Frontend**: Auto-scales on Vercel
- **API Routes**: Serverless, auto-scale
- **Database**: Use connection pooler (PgBouncer)
- **Workers**: Separate execution layer

## 🎨 Customization

### Branding

Edit colors in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
      },
    },
  },
}
```

### Add Pages

1. Create file in `src/pages/`
2. Next.js auto-routes based on file structure
3. Use existing components from `src/components/` (create as needed)

### Add API Endpoints

1. Create file in `src/pages/api/`
2. Export default async function
3. Use `query()` helper from `src/lib/db.ts`

## 🧪 Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build (tests production build)
npm run build
```

## 📊 Monitoring

Add to Vercel:

1. **Analytics**: Vercel Analytics (built-in)
2. **Speed Insights**: Vercel Speed Insights
3. **Logging**: Vercel Logs or Datadog
4. **Errors**: Sentry integration

## 🔐 Security

### Environment Variables

- Never commit `.env.local`
- Use Vercel environment variables for secrets
- Rotate `API_SECRET_KEY` regularly

### Database Access

- Use read-only credentials for display-only queries
- Limit connection pool size
- Use parameterized queries (SQL injection protection)

### API Routes

Consider adding:
- Rate limiting
- Authentication (NextAuth.js)
- API key validation
- CORS configuration

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Deployment](https://vercel.com/docs)
- [PostgreSQL with Vercel](https://vercel.com/guides/using-databases-with-vercel)
- [SWR Documentation](https://swr.vercel.app/)

## 🆘 Troubleshooting

### Database Connection Errors

```bash
# Test connection
psql $DATABASE_URL

# Check Vercel logs
vercel logs
```

### Build Failures

```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### Job Execution Not Working

- Ensure Python CLI is accessible on server
- Check that `cli.py` path is correct in API route
- Consider using job queue for production

## 🎉 Next Steps

1. **Deploy to Vercel** ✅
2. **Add Authentication** (NextAuth.js with Google/GitHub)
3. **Asset Gallery** (View generated images)
4. **Content Preview** (Render blog posts, view scripts)
5. **Real-time WebSockets** (Live job updates)
6. **Admin Dashboard** (Agent management, system stats)
7. **API Documentation** (Swagger/OpenAPI)

---

**Ready to deploy?** Run `vercel` in the `web` directory!
