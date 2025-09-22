# Content Engine V2

🚀 **Professional content creation system with LLM intelligence and real asset generation**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-postgresql-blue.svg)](https://postgresql.org/)
[![Phase 3+](https://img.shields.io/badge/status-phase%203%2B%20complete-brightgreen.svg)](#development-status)
[![Real Generation](https://img.shields.io/badge/capability-real%20content%20generation-gold.svg)](#freepik-integration)

## 🎯 Overview

Content Engine V2 is a **production-ready content creation system** that transforms user requests into professional-quality content across all media types. The system combines LLM intelligence with specialized agents and real API integrations to generate actual content, not just specifications.

### ✨ Key Features

- 🧠 **LLM Intelligence**: Automatic template selection, smart job naming, and context-aware processing
- 🎨 **Real Content Generation**: Professional images via Freepik Mystic API integration
- 📊 **Template-Driven Workflows**: Configurable agent assignments for deterministic results
- 🔄 **Advanced Agent Ecosystem**: 6+ specialized LLM-powered agents with API integrations
- 🎯 **Quality Assurance**: Built-in validation, scoring, and fallback systems
- 💾 **Enterprise Database**: PostgreSQL with comprehensive job tracking and analytics
- 🚀 **Production Scale**: Handle multiple concurrent jobs with cost optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL (or Docker)
- OpenRouter API key (required for LLM intelligence)
- Freepik API key (optional, for real image generation)

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
python cli.py llm-test                # Test LLM integration
python cli.py freepik-test            # Test Freepik API integration
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
│ Template System │    │ Agent Ecosystem │    │ API Integrations│
│ (Agent Control) │    │ (6+ LLM Agents) │    │ (Freepik, etc.) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent Ecosystem

```
BaseAgent (Abstract)
├── PlaceholderAgent (Fallback)
└── LLMAgent (Phase 3 Foundation)
    └── StructuredLLMAgent (JSON Outputs)
        ├── ResearchAgent (X sourcing, analysis)
        ├── WritingAgent (Content creation)
        ├── FreepikMysticAgent (Real image generation) ⭐
        ├── DesignAgent (Image specifications)
        ├── AudioAgent (Audio specifications)
        └── VideoAgent (Video specifications)
```

### Database Schema

- **`jobs`**: Content creation requests with LLM-generated metadata
- **`tasks`**: Individual work items with parameters and preferred agents
- **`agents`**: Processing agents with configurations and API integrations

### Template-Driven Processing Flow

```
User Request → LLM Analysis → Template Selection → Agent Assignment → Real Generation
     ↓              ↓              ↓                    ↓                 ↓
"AI thumbnails" → Content Analysis → top-x-daily-list → FreepikAgent → Professional Images
```

## 📋 Available Templates

| Template | Description | Tasks | Agent Assignments |
|----------|-------------|-------|-------------------|
| `blog-post` | Comprehensive blog articles | 14 | Research + Writing + Design agents |
| `top-x-daily-list` | Daily list videos with real images | 15 | Research + Writing + **Freepik** agents |
| `youtube-tutorial` | Educational video content | 12 | Writing + Design + Audio agents |

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/content_engine

# LLM Integration (Required)
OPENROUTER_API_KEY=your-openrouter-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo
FALLBACK_MODEL=anthropic/claude-3-haiku

# Image Generation APIs (Optional)
FREEPIK_API_KEY=your-freepik-key-here
FREEPIK_WEBHOOK_URL=https://your-domain.com/webhook/freepik

# Audio Generation APIs (Future)
ELEVEN_LABS_API_KEY=your-elevenlabs-key-here

# System Configuration
ASSETS_DIR=./assets
TEMPLATES_DIR=./src/templates/markdown
LOG_LEVEL=INFO
DEBUG=false
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

### ✅ Phase 2: LLM Intelligence (COMPLETE)
- [x] OpenRouter API integration with async support
- [x] Intelligent template selection based on content analysis
- [x] Smart job naming with SEO optimization
- [x] Context-aware agent selection framework
- [x] Cost tracking and usage monitoring
- [x] Graceful fallback when LLM unavailable
- [x] CLI integration with LLM status indicators

### ✅ Phase 3+: Enhanced Agent Ecosystem (COMPLETE)
- [x] **6+ Specialized LLM Agents** across all content categories
- [x] **Real Content Generation** via Freepik Mystic API integration
- [x] **Template-Driven Agent Selection** for deterministic workflows
- [x] **Quality Assurance Systems** with validation and scoring
- [x] **Advanced Prompt Engineering** with structured JSON outputs
- [x] **API Integration Framework** for external service connections
- [x] **Production-Scale Processing** with concurrent job handling
- [x] **Cost Optimization** with intelligent resource management

### 🚀 Phase 4: Production Deployment (READY)
- [x] **Enterprise-Ready Architecture** with comprehensive error handling
- [x] **Scalable Database Design** with performance optimization
- [x] **Professional Quality Outputs** meeting production standards
- [ ] Web interface with React/Next.js (planned)
- [ ] REST API endpoints (planned)
- [ ] Monitoring and analytics dashboard (planned)

## 📊 Example Workflow

```bash
# 1. Test system integrations
$ python cli.py llm-test
🧠 Testing LLM Integration...
✅ LLM Service Status: Connected
🎉 Phase 2+ features are fully operational!

$ python cli.py freepik-test
🎨 Testing Freepik Integration...
✅ Freepik Agent: Freepik Mystic Agent
✅ API Key Configured: True
🎉 Freepik API integration ready!

# 2. Create a job with real image generation
$ python cli.py create "Create daily top 5 AI news with professional thumbnails"
🧠 Using LLM intelligence for template selection...
✓ Job created successfully!
Job ID: c637921e-6a4a-4808-80aa-71561ba96304
Template: top-x-daily-list 🧠 (LLM selected)
Display Name: Daily Top 5 AI News with Professional Thumbnails
Tasks Created: 15 (7 script, 3 image, 2 audio, 3 video)

# 3. Execute with real content generation
$ python cli.py run c637921e-6a4a-4808-80aa-71561ba96304
Processing job: Daily Top 5 AI News with Professional Thumbnails
✅ Research Agent: source_x_posts (score: 0.97)
✅ Writing Agent: write_full_script (score: 0.85)  
✅ Freepik Mystic Agent: design_thumbnail (template-specified) ⭐
✅ Freepik Mystic Agent: create_list_graphics (real images generated)
✓ Job processing completed successfully! 🎉
Professional images created via Freepik API
```

## 🎨 Freepik Integration

### Real Image Generation
The system now generates **actual professional images** using the Freepik Mystic API:

- **YouTube Thumbnails**: Click-optimized, high-contrast, mobile-friendly
- **List Graphics**: Consistent visual series with ranking numbers
- **Social Media Assets**: Platform-specific dimensions and engagement optimization
- **Professional Quality**: Production-ready images at 2K/4K resolution

### Template Control
Templates specify which agents to use:
```markdown
8. **design_thumbnail**
   - Create eye-catching YouTube thumbnail
   - Agent: freepik_mystic  ⭐ Template controls agent selection
   - Parameters: {size: "1280x720", style: "bold", ...}
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
│   ├── engine/         # Content engine and task runner
│   ├── templates/      # Markdown templates with agent specs
│   ├── agents/         # Complete agent ecosystem
│   │   ├── base_agent.py      # Abstract base classes
│   │   ├── llm_agent.py       # LLM-powered agent foundation
│   │   ├── registry.py        # Agent management and selection
│   │   ├── script/            # Research and writing agents
│   │   ├── image/             # Design and Freepik agents
│   │   ├── audio/             # Audio specification agents
│   │   └── video/             # Video specification agents
│   └── llm/            # LLM service integrations
├── docs/               # Comprehensive documentation
├── assets/             # Generated content storage
├── cli.py              # Enhanced CLI with testing commands
└── requirements.txt    # Production dependencies
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🎉 **Content Engine V2: From Ideas to Professional Content**

**Phase 3+ Complete**: LLM intelligence + Real content generation + Template-driven workflows

**🚀 Ready to transform your content creation? Get started with `python cli.py setup`!**

*Generate professional images, research-backed content, and complete multimedia projects - all from a single command.*
