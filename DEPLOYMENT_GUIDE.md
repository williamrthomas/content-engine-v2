# Content Engine V2 - Vercel Deployment Guide

Complete guide to deploying the Content Engine V2 web interface on Vercel.

## 🎯 Overview

This deployment creates a **web interface** for Content Engine V2 that:
- ✅ Displays content jobs and tasks
- ✅ Creates new jobs via web form
- ✅ Triggers job execution
- ✅ Shows real-time progress
- ✅ Shares PostgreSQL database with CLI

## 📋 Prerequisites

Before deploying:

1. ✅ **PostgreSQL Database** - Accessible from internet
   - ✅ Your existing local database can work if publicly accessible
   - ✅ Or use cloud PostgreSQL (Supabase, Neon, AWS RDS, etc.)

2. ✅ **Vercel Account** - Free tier is sufficient
   - Sign up at https://vercel.com

3. ✅ **GitHub Account** (optional but recommended)
   - For automatic deployments

## 🚀 Deployment Steps

### Option A: GitHub + Vercel (Recommended)

This enables automatic deployments on every push.

#### Step 1: Push to GitHub

```bash
# If not already a git repository
cd /home/user/content-engine-v2
git init
git add .
git commit -m "Add Content Engine V2 with web interface"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/content-engine-v2.git
git branch -M main
git push -u origin main
```

#### Step 2: Connect to Vercel

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**: Select your GitHub repo
3. **Configure Project**:
   - **Root Directory**: `web`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

4. **Environment Variables**: Add these:
   ```
   DATABASE_URL = postgresql://user:password@host:5432/content_engine
   ```

5. **Deploy**: Click "Deploy"

#### Step 3: Access Your Site

- Vercel will provide a URL: `https://your-project.vercel.app`
- Test the deployment by creating a job

### Option B: Vercel CLI (Fast & Direct)

Deploy directly from your terminal.

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate.

#### Step 3: Deploy

```bash
cd /home/user/content-engine-v2/web
vercel
```

**During setup, answer:**
- Set up and deploy? **Y**
- Which scope? (Select your account)
- Link to existing project? **N**
- What's your project's name? `content-engine-v2-web`
- In which directory is your code located? **./** (current directory)
- Want to override settings? **N**

#### Step 4: Add Environment Variables

```bash
# After first deployment
vercel env add DATABASE_URL
# Paste your PostgreSQL connection string when prompted

# Redeploy with environment variables
vercel --prod
```

Your site is now live at the URL provided!

## 🔐 Database Configuration

### Option 1: Use Existing Local PostgreSQL

**Requirements:**
- Publicly accessible IP or domain
- PostgreSQL accepts external connections

**Setup:**

1. **Edit PostgreSQL config** (`postgresql.conf`):
   ```
   listen_addresses = '*'
   ```

2. **Edit pg_hba.conf**:
   ```
   host    all    all    0.0.0.0/0    md5
   ```

3. **Restart PostgreSQL**:
   ```bash
   sudo systemctl restart postgresql
   ```

4. **Get your public IP**:
   ```bash
   curl ifconfig.me
   ```

5. **Connection String**:
   ```
   postgresql://username:password@YOUR_PUBLIC_IP:5432/content_engine
   ```

⚠️ **Security Warning**: Only do this if you have proper firewall rules!

### Option 2: Use Cloud PostgreSQL (Recommended)

#### Supabase (Free Tier Available)

1. **Create account**: https://supabase.com
2. **Create new project**
3. **Get connection string**: Settings → Database
4. **Run migrations**:
   ```bash
   psql "YOUR_SUPABASE_CONNECTION_STRING" < schema.sql
   ```

#### Neon (Serverless PostgreSQL)

1. **Create account**: https://neon.tech
2. **Create new project**
3. **Copy connection string**
4. **Run migrations**

#### Railway (Simple & Fast)

1. **Create account**: https://railway.app
2. **New Project** → **Provision PostgreSQL**
3. **Get connection string from Variables tab**

## 🔧 Environment Variables Reference

Add these in **Vercel Dashboard → Settings → Environment Variables**:

### Required

```bash
DATABASE_URL=postgresql://user:password@host:5432/content_engine
```

### Optional

```bash
# API Security (for future auth)
API_SECRET_KEY=generate-random-secret-here

# Public app URL
NEXT_PUBLIC_APP_URL=https://your-project.vercel.app

# For asset serving (if using external storage)
ASSET_BASE_URL=https://your-cdn.com
```

## ✅ Post-Deployment Checklist

1. **Test Database Connection**
   - Visit your site
   - Should see dashboard (may be empty if no jobs)
   - Check Vercel logs if errors occur

2. **Create Test Job**
   - Click "Create Job"
   - Enter: "Write a blog post about AI"
   - Submit
   - Should see job in database

3. **Execute Job** (requires CLI access)
   - Jobs created in web need CLI to execute
   - SSH to your server or run locally:
     ```bash
     python cli.py run <job-id>
     ```
   - Web UI will show updated progress

4. **Set Up Custom Domain** (Optional)
   - Vercel Dashboard → Domains
   - Add your domain (e.g., content.yourdomain.com)
   - Follow DNS configuration steps

## 🏗️ Architecture After Deployment

```
┌─────────────────────────────────────────────────┐
│              Internet Users                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│           Vercel Edge Network                   │
│  ┌───────────────────────────────────────────┐  │
│  │     Next.js Frontend (Static + SSR)      │  │
│  │     - React UI with real-time updates    │  │
│  │     - Auto-deploys on git push           │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │     API Routes (Serverless Functions)    │  │
│  │     - Node.js serverless                 │  │
│  │     - Auto-scale based on traffic        │  │
│  └───────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│        Cloud PostgreSQL Database                │
│        (Shared by Web + CLI)                    │
│        - Jobs, Tasks, Agents tables             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         Your Server / Local Machine             │
│  ┌───────────────────────────────────────────┐  │
│  │     Content Engine CLI (Python)          │  │
│  │     - Executes jobs                      │  │
│  │     - Runs agents (LLM, Freepik, etc.)   │  │
│  │     - Updates database with results      │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 📊 Usage Workflow

### Workflow 1: Web-Initiated Jobs

1. User visits `https://your-project.vercel.app`
2. Creates job via web form
3. Job saved to PostgreSQL with status: `pending`
4. Admin runs CLI to execute: `python cli.py run <job-id>`
5. CLI updates database as tasks complete
6. Web UI auto-refreshes and shows progress

### Workflow 2: CLI-Initiated Jobs

1. User runs CLI: `python cli.py create "Write blog post"`
2. Job created in PostgreSQL
3. User visits web interface
4. Sees job in dashboard
5. Can view progress and results in web UI

## 🔄 Continuous Deployment

After initial setup, deployments are automatic:

```bash
# Make changes to web interface
cd web/src/pages
# Edit files...

# Commit and push
git add .
git commit -m "Update dashboard UI"
git push origin main

# Vercel automatically:
# 1. Detects push
# 2. Builds Next.js app
# 3. Deploys to production
# 4. Takes ~2 minutes
```

## 🐛 Troubleshooting

### Database Connection Fails

**Error**: "Failed to connect to database"

**Solutions**:
1. Check DATABASE_URL is correct in Vercel env vars
2. Ensure database accepts connections from Vercel IPs (all IPs: `0.0.0.0/0`)
3. Test connection locally:
   ```bash
   psql "$DATABASE_URL"
   ```
4. Check Vercel logs: `vercel logs`

### Job Execution Not Working

**Issue**: Jobs stay in "pending" status

**Solution**:
- Web can only CREATE jobs, not EXECUTE them
- You must run CLI to execute: `python cli.py run <job-id>`
- Consider setting up a worker service or cron job

### Build Failures

**Error**: Build fails on Vercel

**Solutions**:
1. Check build logs in Vercel dashboard
2. Test build locally:
   ```bash
   cd web
   npm run build
   ```
3. Ensure all dependencies in package.json
4. Check TypeScript errors: `npm run type-check`

### Page Not Found

**Error**: 404 on routes

**Solution**:
- Ensure files are in correct directories:
  - `src/pages/index.tsx` → `/`
  - `src/pages/jobs/[id].tsx` → `/jobs/:id`
- Clear Vercel cache and redeploy

## 🎨 Customization

### Change Branding

1. Edit `web/tailwind.config.js`:
   ```javascript
   colors: {
     primary: {
       500: '#YOUR_COLOR',
     },
   }
   ```

2. Update text in `web/src/pages/index.tsx`

3. Deploy: `git push` (auto-deploys)

### Add Custom Domain

1. **Vercel Dashboard** → Your Project → Settings → Domains
2. **Add Domain**: `content.yourdomain.com`
3. **Configure DNS** (at your registrar):
   ```
   Type: CNAME
   Name: content
   Value: cname.vercel-dns.com
   ```
4. **Wait for propagation** (~5-60 minutes)
5. **Access**: https://content.yourdomain.com

## 📈 Scaling Considerations

### Current Setup (Good for 0-1000 users/day)

- ✅ Serverless API routes auto-scale
- ✅ Static frontend cached globally
- ⚠️ Database connections limited by pool (max 20)
- ⚠️ Job execution manual (CLI-based)

### Production Upgrades (For 1000+ users/day)

1. **Connection Pooler**: PgBouncer or Supabase Pooler
2. **Job Queue**: BullMQ, Celery, or AWS SQS
3. **Worker Service**: Dedicated workers for job execution
4. **CDN**: Cloudflare for assets and API caching
5. **Monitoring**: Datadog, New Relic, or Vercel Analytics
6. **Authentication**: NextAuth.js with Google/GitHub OAuth

## 🎉 You're Done!

Your Content Engine V2 is now deployed and accessible worldwide!

**Quick Links**:
- 🌐 **Production Site**: https://your-project.vercel.app
- 📊 **Vercel Dashboard**: https://vercel.com/dashboard
- 🔧 **Settings**: https://vercel.com/YOUR_USERNAME/YOUR_PROJECT/settings
- 📝 **Logs**: `vercel logs` or dashboard

**Next Steps**:
1. Share the URL with your team
2. Set up monitoring and alerts
3. Configure custom domain
4. Add authentication if needed
5. Set up automated job execution

Need help? Check the `web/README.md` or create an issue on GitHub.

---

**Happy deploying! 🚀**
