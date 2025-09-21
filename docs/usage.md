# Content Engine V2 - Usage Guide

## Quick Start

### 1. Create Your First Job

```bash
# Create a blog post
python cli.py create "Write a comprehensive blog post about sustainable energy solutions"

# Create with specific template
python cli.py create "Tutorial on Python basics" --template youtube-tutorial

# Dry run to see what would be created
python cli.py create "Test content" --dry-run
```

### 2. Check Job Status

```bash
# Check specific job status
python cli.py status <job-id>

# List all jobs
python cli.py list jobs

# List only pending jobs
python cli.py list jobs --status pending
```

### 3. Process Jobs

```bash
# Process a job (execute all tasks)
python cli.py process <job-id>

# Process with real-time monitoring
python cli.py process <job-id> --monitor
```

## CLI Commands Reference

### Job Management

#### `create` - Create New Job
```bash
python cli.py create "Your content request"
```

**Options:**
- `--template, -t` - Specify template (blog-post, youtube-tutorial)
- `--dry-run` - Preview without creating

**Examples:**
```bash
python cli.py create "Blog about AI trends" --template blog-post
python cli.py create "How to use Docker" --template youtube-tutorial
python cli.py create "Test content" --dry-run
```

#### `status` - Check Job Status
```bash
python cli.py status <job-id>
```

Shows detailed job information including:
- Job metadata (name, status, template)
- Task breakdown by category
- Individual task status
- Execution timeline

#### `process` - Execute Job Tasks
```bash
python cli.py process <job-id>
```

**Options:**
- `--monitor, -m` - Real-time progress monitoring

Executes all job tasks in sequential order:
1. Script tasks (research, writing, optimization)
2. Image tasks (graphics, thumbnails, social images)
3. Audio tasks (narration, music, effects)
4. Video tasks (editing, rendering, optimization)

#### `list` - List Jobs
```bash
python cli.py list jobs
```

**Options:**
- `--status, -s` - Filter by status (pending, in_progress, completed, failed)
- `--limit, -l` - Maximum jobs to show (default: 20)

### Template Management

#### `templates list` - Show Available Templates
```bash
python cli.py templates list
```

#### `templates validate` - Validate Template
```bash
python cli.py templates validate blog-post
```

### Database Management

#### `db init` - Initialize Database
```bash
python cli.py db init
```

#### `db status` - Database Health Check
```bash
python cli.py db status
```

### System Management

#### `config` - Show Configuration
```bash
python cli.py config
```

## Working with Templates

### Available Templates

#### Blog Post (`blog-post`)
- **Purpose**: Comprehensive blog articles with SEO optimization
- **Tasks**: 14 tasks across all categories
- **Best for**: Articles, guides, informational content

#### YouTube Tutorial (`youtube-tutorial`)
- **Purpose**: Educational video content with supporting materials
- **Tasks**: 12 tasks focused on video production
- **Best for**: Tutorials, how-to videos, educational content

### Template Selection

The system automatically selects templates based on keywords in your request:

- **Blog/Article keywords**: "blog", "article", "post", "write" → `blog-post`
- **Video keywords**: "video", "tutorial", "youtube", "teach" → `youtube-tutorial`
- **Manual selection**: Use `--template` flag

### Custom Templates

Create new templates in `src/templates/markdown/`:

```markdown
# My Custom Template

**Category**: custom
**Target Duration**: 30 minutes

## Tasks

### Script Tasks
1. **custom_task**
   - Task description
   - Parameters: {param1: value1, param2: value2}
```

## Understanding Job Execution

### Sequential Processing

Jobs execute in strict category order:
1. **Script** → 2. **Image** → 3. **Audio** → 4. **Video**

Within each category, tasks execute by sequence order.

### Task Parameters

Each task receives:
- **Inputs**: User request, previous task outputs, job context
- **Requirements**: Template-defined parameters
- **Outputs**: Generated content, files, metadata

### Phase 1 Behavior

Currently using placeholder agents that:
- Generate realistic sample outputs
- Simulate processing time
- Demonstrate the full workflow
- Prepare for real agent integration in Phase 2

## Monitoring and Debugging

### Job Status Indicators

- 🟡 **Pending**: Job created, waiting to process
- 🔄 **In Progress**: Currently executing tasks
- ✅ **Completed**: All tasks finished successfully
- ❌ **Failed**: One or more tasks failed

### Task Status Indicators

- ⏳ **Pending**: Task waiting to execute
- 🔄 **In Progress**: Task currently running
- ✅ **Completed**: Task finished successfully
- ❌ **Failed**: Task execution failed

### Logs and Debugging

- Check `content_engine.log` for detailed execution logs
- Use `--dry-run` to preview job creation
- Use `--monitor` to watch real-time progress
- Check database status with `python cli.py db status`

## Best Practices

### Job Creation

1. **Be specific** in your requests for better template selection
2. **Use templates** explicitly when you know what you want
3. **Test with dry-run** before creating large jobs

### Job Processing

1. **Monitor progress** for long-running jobs
2. **Check status** before reprocessing failed jobs
3. **Review outputs** in task parameters after completion

### System Maintenance

1. **Regular database health checks**: `python cli.py db status`
2. **Template validation**: `python cli.py templates validate <name>`
3. **Configuration review**: `python cli.py config`

## Troubleshooting

### Common Issues

#### "Database connection failed"
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Run `python cli.py db init` to initialize schema

#### "Template not found"
- Check available templates: `python cli.py templates list`
- Validate template syntax: `python cli.py templates validate <name>`
- Ensure template files exist in `src/templates/markdown/`

#### "Job processing failed"
- Check job status for specific task failures
- Review logs in `content_engine.log`
- Verify all required parameters are provided

#### "Invalid job ID"
- Use full UUID from job creation or status command
- Check job exists: `python cli.py list jobs`

### Getting Help

- Use `--help` with any command for detailed options
- Check logs for detailed error information
- Review configuration with `python cli.py config`
