# Content Engine V2 - Complete Project Plan

## 🎯 **Project Overview**

Building an **LLM-orchestrated content creation system** with PostgreSQL backend, Python CLI interface, and intelligent agent selection. The system processes jobs sequentially (script → image → audio → video) with LLM decision-making at every step.

## 🏆 **Phase 1: COMPLETE** ✅

**Status**: All Phase 1 deliverables achieved and system fully functional!

### ✅ **Completed Features**
- **Database**: PostgreSQL with 3-table schema, full CRUD operations, JSONB handling
- **CLI**: Beautiful Typer+Rich interface with all core commands working
- **Templates**: 2 markdown templates with auto-selection (blog-post, youtube-tutorial)
- **Processing**: Sequential job execution with placeholder agents
- **Architecture**: Complete async/await implementation with connection pooling

### ✅ **Working Commands**
- `python cli.py create "request"` - Job creation with template auto-selection
- `python cli.py run <job-id>` - Execute jobs sequentially
- `python cli.py list` - Beautiful job listing with status
- `python cli.py status <job-id>` - Detailed job/task information
- `python cli.py templates` - Show available templates
- `python cli.py setup` - System initialization
- `python cli.py help` - Comprehensive usage guide

**Ready for Phase 2 LLM integration!** 🚀

## 🛠️ **Final Tech Stack**

### **Core Technologies**
- **Language**: Python 3.9+ (async/await, type hints)
- **Database**: PostgreSQL with asyncpg driver
- **LLM Provider**: OpenRouter (gpt-3.5-turbo for testing)
- **CLI Framework**: Typer + Rich (beautiful, modern CLI)
- **Storage**: Local filesystem with organized structure

### **Key Dependencies**
```python
# Core Framework
typer>=0.9.0           # Modern CLI framework
rich>=13.0.0           # Beautiful terminal output
asyncio                # Async execution
asyncpg>=0.28.0        # PostgreSQL async driver

# LLM & HTTP
openai>=1.0.0          # OpenRouter API client
aiohttp>=3.8.0         # Async HTTP requests
httpx>=0.24.0          # Alternative HTTP client

# Data & Storage
pydantic>=2.0.0        # Data validation
python-dotenv>=1.0.0   # Environment management
aiofiles>=23.0.0       # Async file operations
pathlib                # Path management

# Utilities
uuid                   # Job/task IDs
json                   # Data serialization
logging                # System observability
colorama>=0.4.6        # Cross-platform colors
```

## 📁 **Project Structure**

```
content-engine-v2/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── cli.py                    # Main CLI entry point
├── 
├── src/
│   ├── __init__.py
│   ├── 
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py       # PostgreSQL connection & queries
│   │   ├── models.py         # Pydantic data models
│   │   └── config.py         # Configuration management
│   ├── 
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── content_engine.py # Main orchestration class
│   │   ├── task_runner.py    # Sequential task execution
│   │   └── llm_services.py   # Template/agent selection via LLM
│   ├── 
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py     # Base agent class
│   │   ├── script/
│   │   │   ├── __init__.py
│   │   │   ├── gpt35_agent.py
│   │   │   └── claude_haiku_agent.py
│   │   ├── image/
│   │   │   ├── __init__.py
│   │   │   └── placeholder_agent.py
│   │   ├── audio/
│   │   │   ├── __init__.py
│   │   │   └── placeholder_agent.py
│   │   └── video/
│   │       ├── __init__.py
│   │       └── placeholder_agent.py
│   ├── 
│   └── templates/
│       ├── __init__.py
│       ├── loader.py         # Template parsing from markdown
│       └── markdown/         # Template files
│           ├── blog-post.md
│           ├── youtube-tutorial.md
│           └── podcast-episode.md
├── 
├── assets/                   # Generated content storage
│   └── jobs/
│       └── {job-name}/
│           ├── script/
│           ├── images/
│           ├── audio/
│           └── video/
├── 
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_engine.py
│   └── test_agents.py
├── 
└── docs/
    ├── setup.md
    ├── usage.md
    └── api.md
```

## 🚀 **4-Phase Development Plan**

### **Phase 1: Foundation (Week 1)**
**Goal**: Basic working system with PostgreSQL and CLI

#### **Day 1-2: Database & Core Setup**
- [ ] PostgreSQL database setup with Docker
- [ ] Database schema creation (jobs, tasks, agents tables)
- [ ] Core models with Pydantic
- [ ] Database connection and basic queries
- [ ] Environment configuration

#### **Day 3-4: CLI Framework**
- [ ] Typer CLI setup with Rich output
- [ ] Basic commands: `create`, `status`, `list`
- [ ] Configuration management
- [ ] Logging setup with Rich console

#### **Day 5-7: Template System**
- [ ] Markdown template parser
- [ ] Template loading and validation
- [ ] Job creation from templates
- [ ] Basic task generation

**Deliverable**: CLI that can create jobs from templates and store in PostgreSQL

### **Phase 2: LLM Intelligence (Week 2)**
**Goal**: LLM-powered template and agent selection

#### **Day 8-9: OpenRouter Integration**
- [ ] OpenRouter client setup
- [ ] Basic LLM service for template selection
- [ ] Error handling and retry logic
- [ ] Cost tracking and monitoring

#### **Day 10-11: Intelligent Selection**
- [ ] LLM template selection service
- [ ] LLM job naming service
- [ ] Agent selection framework
- [ ] Context-aware parameter population

#### **Day 12-14: Task Runner**
- [ ] Sequential task execution engine
- [ ] Task status management
- [ ] Progress tracking with Rich progress bars
- [ ] Basic error handling

**Deliverable**: System that intelligently selects templates and processes tasks

### **Phase 3: Agent Ecosystem (Week 3)**
**Goal**: Multiple agents across all categories

#### **Day 15-16: Script Agents**
- [ ] GPT-3.5-turbo script agent
- [ ] Claude Haiku script agent
- [ ] Agent selection logic
- [ ] Output standardization

#### **Day 17-18: Media Agents (Placeholders)**
- [ ] Image generation placeholder agent
- [ ] Audio generation placeholder agent
- [ ] Video generation placeholder agent
- [ ] File management system

#### **Day 19-21: Agent Management**
- [ ] Agent registration system
- [ ] Agent configuration management
- [ ] Agent health monitoring
- [ ] Dynamic agent loading

**Deliverable**: Multi-agent system with intelligent selection

### **Phase 4: Production Ready (Week 4)**
**Goal**: Robust, monitorable, production-ready system

#### **Day 22-23: Monitoring & Logging**
- [ ] Comprehensive logging system
- [ ] Job progress monitoring
- [ ] Performance metrics
- [ ] Error tracking and reporting

#### **Day 24-25: Asset Management**
- [ ] Organized file storage system
- [ ] Asset metadata tracking
- [ ] File cleanup and archiving
- [ ] Storage optimization

#### **Day 26-28: Polish & Documentation**
- [ ] CLI help and documentation
- [ ] Error message improvements
- [ ] Performance optimization
- [ ] Testing and validation
- [ ] Deployment documentation

**Deliverable**: Production-ready Content Engine V2

## 🎨 **CLI Interface Design**

### **Main Commands**
```bash
# Job Management
content-engine create "Blog post about AI trends"
content-engine status job-123
content-engine process job-123
content-engine monitor job-123
content-engine list jobs --status pending

# Template Management
content-engine templates list
content-engine templates reload
content-engine templates validate blog-post.md

# Agent Management
content-engine agents list --category script
content-engine agents add script gpt4 --config config.json
content-engine agents test gpt35_script

# System Management
content-engine db init
content-engine db migrate
content-engine db status
content-engine config show
```

### **Rich CLI Features**
- **Colorful status indicators** (🟢 completed, 🟡 in-progress, 🔴 failed)
- **Progress bars** for job execution
- **Beautiful tables** for job/agent listings
- **Syntax highlighting** for template validation
- **Interactive prompts** for configuration

## 🗄️ **Database Schema**

```sql
-- Jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    display_name VARCHAR(200),
    template_name VARCHAR(100),
    user_request TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Tasks table  
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    task_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    sequence_order INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    assigned_agent_id UUID,
    parameters JSONB NOT NULL DEFAULT '{}',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Agents table
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    instance_key VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(20) NOT NULL,
    provider VARCHAR(50),
    model VARCHAR(50),
    specialization TEXT,
    config JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## ⚙️ **Configuration**

### **.env Template**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/content_engine

# LLM
OPENROUTER_API_KEY=sk-or-...
DEFAULT_MODEL=openai/gpt-3.5-turbo
FALLBACK_MODEL=anthropic/claude-3-haiku

# Storage
ASSETS_DIR=./assets
TEMPLATES_DIR=./src/templates/markdown

# Logging
LOG_LEVEL=INFO
LOG_FILE=content_engine.log

# CLI
CLI_THEME=dark
PROGRESS_BARS=true
```

## 🎯 **Success Metrics**

### **Phase 1 Success**
- [ ] PostgreSQL database operational
- [ ] CLI creates jobs from templates
- [ ] Basic task storage and retrieval
- [ ] Rich CLI output working

### **Phase 2 Success**
- [ ] LLM selects appropriate templates
- [ ] Jobs have intelligent names
- [ ] Tasks execute sequentially
- [ ] Progress tracking functional

### **Phase 3 Success**
- [ ] Multiple script agents working
- [ ] Agent selection logic operational
- [ ] Placeholder agents for all categories
- [ ] File management system working

### **Phase 4 Success**
- [ ] Comprehensive monitoring
- [ ] Production-ready error handling
- [ ] Complete documentation
- [ ] Performance optimized

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.9+
- PostgreSQL 14+
- OpenRouter API key

### **Quick Setup**
```bash
# Clone and setup
git clone <repo>
cd content-engine-v2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database setup
createdb content_engine
python -m src.core.database init

# Configuration
cp .env.example .env
# Edit .env with your settings

# Test run
python cli.py --help
python cli.py create "Test blog post"
```

This plan provides a **complete roadmap** from foundation to production-ready system, with clear milestones and deliverables at each phase.
