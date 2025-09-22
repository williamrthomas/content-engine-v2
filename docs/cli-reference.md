# CLI Reference Guide

## 🚀 **Complete Command-Line Interface Reference**

Content Engine V2 provides a comprehensive CLI built with Typer and Rich for beautiful, intuitive content creation workflows.

## 📋 **Command Overview**

### **Core Commands**
- [`setup`](#setup) - Initialize system and database
- [`create`](#create) - Create new content jobs
- [`run`](#run) - Execute job tasks
- [`status`](#status) - Check job status and details
- [`list`](#list) - Show recent jobs

### **System Commands**
- [`templates`](#templates) - Show available templates
- [`llm-test`](#llm-test) - Test LLM integration
- [`freepik-test`](#freepik-test) - Test Freepik API integration
- [`help`](#help) - Show detailed usage guide

---

## 🔧 **Command Details**

### `setup`
Initialize the Content Engine system and database.

```bash
python cli.py setup
```

**What it does:**
- Creates PostgreSQL database schema
- Initializes agent registry
- Validates configuration
- Sets up directory structure
- Tests core integrations

**Example Output:**
```
🚀 Content Engine V2 Setup
✅ Database connection established
✅ Schema created successfully
✅ Agent registry initialized (7 agents)
✅ Templates loaded (3 templates)
✅ LLM integration verified
🎉 Setup completed successfully!
```

---

### `create`
Create new content generation jobs with LLM-powered template selection.

```bash
python cli.py create "DESCRIPTION" [OPTIONS]
```

**Arguments:**
- `DESCRIPTION` - Natural language description of content to create

**Options:**
- `--template TEXT` - Force specific template (bypasses LLM selection)
- `--help` - Show command help

**Examples:**

```bash
# LLM will auto-select template
python cli.py create "Write a blog post about sustainable energy"
python cli.py create "Create daily top 5 AI news with thumbnails"
python cli.py create "Make a YouTube tutorial on Docker containers"

# Force specific template
python cli.py create "AI tutorial" --template youtube-tutorial
```

**Output:**
```
🧠 Using LLM intelligence for template selection...
✓ Job created successfully!
Job ID: c637921e-6a4a-4808-80aa-71561ba96304
Job Name: daily-ai-news-with-thumbnails
Template: top-x-daily-list 🧠 (LLM selected)
Tasks Created: 15 (7 script, 3 image, 2 audio, 3 video)

💡 Next: python cli.py run c637921e-6a4a-4808-80aa-71561ba96304
```

---

### `run`
Execute job tasks with real content generation.

```bash
python cli.py run JOB_ID
```

**Arguments:**
- `JOB_ID` - UUID of the job to execute

**Examples:**
```bash
python cli.py run c637921e-6a4a-4808-80aa-71561ba96304
```

**Process Flow:**
1. **Script Tasks**: Research, writing, content creation
2. **Image Tasks**: Design specifications or real image generation
3. **Audio Tasks**: Narration and music specifications
4. **Video Tasks**: Editing and platform optimization

**Live Output:**
```
Processing job: Daily AI News with Thumbnails
Job ID: c637921e-6a4a-4808-80aa-71561ba96304
Tasks: 15

✅ Research Agent: source_x_posts (score: 0.97)
✅ Writing Agent: write_full_script (score: 0.85)
✅ Freepik Mystic Agent: design_thumbnail (template-specified)
✅ Freepik Mystic Agent: create_list_graphics (real images generated)

✓ Job processing completed successfully! 🎉
Final status: completed
Tasks completed: 15
```

---

### `status`
Check detailed job status and task progress.

```bash
python cli.py status JOB_ID
```

**Arguments:**
- `JOB_ID` - UUID of the job to check

**Examples:**
```bash
python cli.py status c637921e-6a4a-4808-80aa-71561ba96304
```

**Output:**
```
┌─ Job Details ─┐
│ ID: c637921e-6a4a-4808-80aa-71561ba96304
│ Name: daily-ai-news-with-thumbnails
│ Display: Daily AI News with Thumbnails
│ Template: top-x-daily-list
│ Status: completed
│ Created: 2025-09-21 19:11:08
│ Completed: 2025-09-21 19:13:45
└───────────────┘

📊 Task Breakdown:
  ✅ script: 7/7 completed
  ✅ image: 3/3 completed  
  ✅ audio: 2/2 completed
  ✅ video: 3/3 completed

🎯 Agent Performance:
  • Research Agent: 3 tasks (avg score: 0.91)
  • Writing Agent: 4 tasks (avg score: 0.87)
  • Freepik Mystic Agent: 3 tasks (real generation)
  • Audio Agent: 2 tasks (specifications)
  • Video Agent: 3 tasks (specifications)
```

---

### `list`
Show recent jobs with status and summary.

```bash
python cli.py list [OPTIONS]
```

**Options:**
- `--limit INTEGER` - Number of jobs to show (default: 10)
- `--status TEXT` - Filter by status (pending, running, completed, failed)

**Examples:**
```bash
python cli.py list
python cli.py list --limit 5
python cli.py list --status completed
```

**Output:**
```
📋 Recent Jobs

┌─────────────────────────────────────┬──────────────────────────────┬───────────┬─────────┐
│ Job ID                              │ Name                         │ Template  │ Status  │
├─────────────────────────────────────┼──────────────────────────────┼───────────┼─────────┤
│ c637921e-6a4a-4808-80aa-71561ba96304│ daily-ai-news-with-thumbnails│ top-x-... │completed│
│ 86f080ba-c9fd-4e57-953c-cd4cb999784f│ ai-breakthroughs-top-5       │ top-x-... │running  │
│ 65eff2df-312e-46df-9413-d095e934a9ed│ sustainable-energy-guide     │ blog-post │pending  │
└─────────────────────────────────────┴──────────────────────────────┴───────────┴─────────┘

💡 Use 'python cli.py status <job-id>' for detailed information
```

---

### `templates`
Show available content templates and their capabilities.

```bash
python cli.py templates
```

**Output:**
```
📋 Available Templates

┌─────────────────┬─────────────────────────────────┬───────┬──────────────────────┐
│ Template        │ Description                     │ Tasks │ Agent Assignments    │
├─────────────────┼─────────────────────────────────┼───────┼──────────────────────┤
│ blog-post       │ Comprehensive blog articles     │ 14    │ Research + Writing   │
│ top-x-daily-list│ Daily list videos with images   │ 15    │ Research + Freepik   │
│ youtube-tutorial│ Educational video content       │ 12    │ Writing + Design     │
└─────────────────┴─────────────────────────────────┴───────┴──────────────────────┘

🎯 Template Selection:
  • Automatic: LLM analyzes your request and selects best template
  • Manual: Use --template flag to force specific template
  • Custom: Create your own templates in src/templates/markdown/

💡 Templates control which agents are used for each task
```

---

### `llm-test`
Test LLM service connectivity and capabilities.

```bash
python cli.py llm-test
```

**What it tests:**
- OpenRouter API connection
- Model availability and access
- Template selection capabilities
- Job naming functionality
- Usage statistics and costs

**Output:**
```
🧠 Testing LLM Integration...
✅ LLM Service Status: Connected
Status: operational
Model: openai/gpt-3.5-turbo

📊 Usage Statistics:
  Total requests: 1,247
  Total tokens: 892,156
  Estimated cost: $1.2847

🎉 Phase 2+ features are fully operational!
• Intelligent template selection
• Smart job naming
• Context-aware processing
```

---

### `freepik-test`
Test Freepik Mystic API integration for real image generation.

```bash
python cli.py freepik-test
```

**What it tests:**
- Freepik API key validation
- Agent availability and configuration
- Sample image generation capability
- Quality scoring and validation

**Output:**
```
🎨 Testing Freepik Integration...
✅ Freepik Agent: Freepik Mystic Agent
API Key Configured: True
Specializations: 8

Test Execution: TaskStatus.COMPLETED
Quality Score: 0.8

🎉 Freepik API integration ready!
• Real image generation enabled
• Professional quality output
• Multi-format support
```

**Without API Key:**
```
🎨 Testing Freepik Integration...
✅ Freepik Agent: Freepik Mystic Agent
API Key Configured: False

📋 Specification mode active
• Detailed prompts generated
• API parameters optimized
• Ready for manual generation

💡 To enable image generation:
export FREEPIK_API_KEY=your-api-key-here
```

---

### `help`
Show comprehensive usage guide and examples.

```bash
python cli.py help
```

**Output:**
```
🚀 Content Engine V2 - Complete Usage Guide

📋 QUICK START:
  1. python cli.py setup                    # Initialize system
  2. python cli.py create "Your request"    # Create job
  3. python cli.py run <job-id>             # Execute job

🎯 COMMON WORKFLOWS:
  Blog Posts:
    python cli.py create "Write about sustainable energy trends"
    
  YouTube Content:
    python cli.py create "Docker tutorial for beginners"
    
  Daily Lists:
    python cli.py create "Top 5 AI breakthroughs today"

🔧 SYSTEM TESTING:
  python cli.py llm-test        # Test LLM integration
  python cli.py freepik-test    # Test image generation
  python cli.py templates       # Show available templates

📊 JOB MANAGEMENT:
  python cli.py list            # Show recent jobs
  python cli.py status <id>     # Check job details
  python cli.py run <id>        # Execute job tasks

💡 For detailed command help: python cli.py COMMAND --help
```

---

## 🎯 **Usage Patterns**

### **Complete Workflow**
```bash
# 1. Setup (one-time)
python cli.py setup

# 2. Test integrations
python cli.py llm-test
python cli.py freepik-test

# 3. Create content
python cli.py create "Create professional YouTube thumbnail for AI news"

# 4. Execute job
python cli.py run <job-id>

# 5. Check results
python cli.py status <job-id>
```

### **Development Workflow**
```bash
# Test new templates
python cli.py templates

# Create test job
python cli.py create "Test content" --template blog-post

# Monitor execution
python cli.py run <job-id>
python cli.py status <job-id>

# Review recent jobs
python cli.py list --limit 5
```

### **Production Workflow**
```bash
# Batch job creation
python cli.py create "Daily AI news #1"
python cli.py create "Daily AI news #2"
python cli.py create "Daily AI news #3"

# Check job queue
python cli.py list --status pending

# Execute jobs
for job_id in $(python cli.py list --status pending --format ids); do
  python cli.py run $job_id
done
```

---

## 🚀 **Advanced Usage**

### **Environment-Specific Commands**
```bash
# Development
DEBUG=true python cli.py create "Test job"

# Production
LOG_LEVEL=WARNING python cli.py run <job-id>

# With specific API keys
FREEPIK_API_KEY=key python cli.py freepik-test
```

### **Automation & Scripting**
```bash
#!/bin/bash
# Daily content generation script

# Create daily jobs
JOB1=$(python cli.py create "Daily AI news" --format id)
JOB2=$(python cli.py create "Tech trends summary" --format id)

# Execute jobs
python cli.py run $JOB1
python cli.py run $JOB2

# Report status
python cli.py status $JOB1
python cli.py status $JOB2
```

---

## 💡 **Tips & Best Practices**

### **Job Creation**
- **Be Specific**: "Create YouTube thumbnail for AI tutorial" vs "Make image"
- **Include Context**: "Daily top 5 AI news with professional thumbnails"
- **Use Keywords**: LLM uses keywords for template selection

### **Template Selection**
- **Let LLM Choose**: Usually selects the best template automatically
- **Override When Needed**: Use `--template` for specific requirements
- **Test Templates**: Use `python cli.py templates` to see options

### **Monitoring Jobs**
- **Check Status Regularly**: Use `python cli.py status <id>`
- **Review Agent Performance**: Look at quality scores
- **Monitor Costs**: Check LLM usage statistics

### **API Management**
- **Test Integrations**: Run test commands before production
- **Monitor API Limits**: Check usage and rate limits
- **Backup Keys**: Store API keys securely

---

**🎉 The CLI provides complete control over the Content Engine V2 system with beautiful, intuitive commands for every workflow!**
