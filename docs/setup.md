# Content Engine V2 - Setup Guide

## Prerequisites

- **Python 3.9+** - Required for modern async/await and type hints
- **PostgreSQL 14+** - Database backend
- **OpenRouter API Key** - For LLM services

## Installation

### 1. Clone and Setup Environment

```bash
cd content-engine-v2
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb content_engine

# Initialize schema
python cli.py db init
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENROUTER_API_KEY` - Your OpenRouter API key

### 4. Verify Installation

```bash
# Check system status
python cli.py db status

# List available templates
python cli.py templates list

# Show configuration
python cli.py config
```

## Development Setup

### Additional Dependencies

```bash
pip install pytest pytest-asyncio black
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ cli.py tests/
```

## Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check DATABASE_URL format: `postgresql://user:password@localhost:5432/content_engine`
3. Ensure database exists: `createdb content_engine`

### Template Loading Issues

1. Verify templates directory exists: `src/templates/markdown/`
2. Check template syntax with: `python cli.py templates validate template-name`

### API Key Issues

1. Get OpenRouter API key from: https://openrouter.ai/
2. Set in .env file: `OPENROUTER_API_KEY=sk-or-your-key-here`
