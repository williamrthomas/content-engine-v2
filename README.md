# Content Engine V2

🚀 **LLM-orchestrated content creation system with sequential task processing**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql-blue.svg)](https://postgresql.org/)
[![Phase 1](https://img.shields.io/badge/status-phase%201%20complete-green.svg)](#development-status)

## 🎯 Overview

Content Engine V2 is a sophisticated content creation system that uses Large Language Models (LLMs) to intelligently orchestrate the creation of multi-media content. The system breaks down content requests into sequential tasks across four categories: **script → image → audio → video**.

### ✨ Key Features

- 🧠 **LLM-Powered Intelligence**: Automatic template selection and job naming
- 📊 **Sequential Processing**: Strict task execution order ensures content coherence
- 🎨 **Beautiful CLI**: Rich, colorful interface with helpful guidance
- 📋 **Template System**: Markdown-based templates with auto-selection
- 🔄 **Agent Framework**: Specialized agents for different content types
- 💾 **PostgreSQL Backend**: Robust 3-table design with JSONB flexibility

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL (or Docker)
- OpenRouter API key (for Phase 2)

### Installation

```bash
# 1. Clone and setup
git clone <repository-url>
cd content-engine-v2-claude
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database URL and API key

# 4. Initialize system
python cli.py setup
```

### 🎮 Usage

```bash
# Create content jobs
python cli.py create "Write a blog post about AI trends"
python cli.py create "Make a YouTube tutorial on Docker" --template youtube-tutorial

# Manage jobs
python cli.py list                    # Show recent jobs
python cli.py status <job-id>         # Check job details
python cli.py run <job-id>            # Execute job tasks

# System commands
python cli.py templates               # Show available templates
python cli.py help                    # Detailed usage guide
```

## 🏗️ Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Content Engine │    │   PostgreSQL    │
│   (Typer+Rich) │◄──►│   (Async Core)  │◄──►│   (3 Tables)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Template System │    │ Agent Framework │    │ Job Processing  │
│   (Markdown)    │    │  (Placeholder)  │    │  (Sequential)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Database Schema

- **`jobs`**: Content creation requests with metadata
- **`tasks`**: Individual work items with parameters (JSONB)
- **`agents`**: Processing agents with configurations (JSONB)

### Sequential Processing Flow

```
User Request → Template Selection → Task Creation → Sequential Execution
     ↓              ↓                    ↓               ↓
"Blog post"    blog-post.md        14 tasks      script→image→audio→video
```

## 📋 Available Templates

| Template | Description | Tasks | Categories |
|----------|-------------|-------|------------|
| `blog-post` | Comprehensive blog articles | 14 | script: 7, image: 3, audio: 2, video: 2 |
| `youtube-tutorial` | Educational video content | 12 | script: 5, image: 3, audio: 2, video: 2 |

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/content_engine

# LLM Integration (Phase 2)
OPENROUTER_API_KEY=your-api-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo

# System
ASSETS_DIR=./assets
TEMPLATES_DIR=./src/templates/markdown
LOG_LEVEL=INFO
```

### Docker Database Setup

```bash
# Quick PostgreSQL setup
docker run --name content-engine-db \
  -e POSTGRES_PASSWORD=your-password \
  -p 5432:5432 \
  -v content_engine_data:/var/lib/postgresql/data \
  -d postgres
```

## 🎯 Development Status

### ✅ Phase 1: Foundation (COMPLETE)
- [x] PostgreSQL database with 3-table schema
- [x] Complete Pydantic data models with type safety
- [x] Typer + Rich CLI with beautiful interface
- [x] Markdown template system with auto-selection
- [x] Sequential task processing engine
- [x] Base agent framework with placeholder implementations
- [x] Full job lifecycle management
- [x] Comprehensive documentation and setup

### 🔄 Phase 2: LLM Intelligence (NEXT)
- [ ] OpenRouter API integration
- [ ] Intelligent template selection based on content analysis
- [ ] Smart job naming with SEO optimization
- [ ] Context-aware agent selection
- [ ] Cost tracking and usage monitoring

### 🚧 Phase 3: Agent Ecosystem (PLANNED)
- [ ] Real agent implementations for each category
- [ ] Multi-provider support (OpenAI, Anthropic, etc.)
- [ ] Quality monitoring and validation
- [ ] Cost optimization strategies

### 🎉 Phase 4: Production Ready (PLANNED)
- [ ] Web interface with React/Next.js
- [ ] REST API endpoints
- [ ] Monitoring and analytics dashboard
- [ ] Deployment automation and scaling

## 📊 Example Workflow

```bash
# 1. Create a job
$ python cli.py create "Write a comprehensive guide about sustainable energy"
✓ Job created: 139c7ad8-ac11-492d-9e40-c76835e6ec09
✓ Template: blog-post (auto-selected)
✓ Tasks: 14 created

# 2. Check status
$ python cli.py status 139c7ad8-ac11-492d-9e40-c76835e6ec09
┌─ Job Details ─┐
│ Name: Write a comprehensive guide about sustainable energy
│ Status: pending
│ Tasks: 14 (7 script, 3 image, 2 audio, 2 video)
└───────────────┘

# 3. Execute job
$ python cli.py run 139c7ad8-ac11-492d-9e40-c76835e6ec09
✓ Job processing completed successfully! 🎉
Final status: completed
Tasks completed: 14
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Submit a pull request

## 📁 Project Structure

```
content-engine-v2/
├── src/
│   ├── core/           # Database, models, config
│   ├── engine/         # Main content engine
│   ├── templates/      # Markdown templates
│   └── agents/         # Agent implementations
├── assets/             # Generated content
├── archive/            # Legacy development files
├── cli.py              # Main CLI interface
├── setup.py            # System initialization
└── requirements.txt    # Dependencies
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🚀 Ready to create amazing content? Get started with `python cli.py help`!**
