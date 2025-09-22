# Configuration Guide

## 🔧 **Complete Configuration Reference**

Content Engine V2 uses environment variables for configuration, providing flexibility for different deployment environments while maintaining security best practices.

## 📋 **Configuration Overview**

### **Configuration Sources**
1. **Environment Variables** - Primary configuration method
2. **`.env` File** - Local development convenience
3. **System Defaults** - Fallback values for optional settings

### **Configuration Categories**
- **Database**: PostgreSQL connection settings
- **LLM Integration**: OpenRouter API configuration
- **Image Generation**: Freepik API settings
- **Audio Generation**: ElevenLabs API settings (future)
- **System**: Logging, directories, and operational settings

---

## 🗄️ **Database Configuration**

### **DATABASE_URL** (Required)
PostgreSQL connection string for the main database.

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Examples:**
```bash
# Local development
DATABASE_URL=postgresql://postgres:password@localhost:5432/content_engine

# Docker container
DATABASE_URL=postgresql://postgres:password@content-engine-db:5432/content_engine

# Cloud database (Heroku, AWS RDS, etc.)
DATABASE_URL=postgresql://user:pass@host.region.rds.amazonaws.com:5432/content_engine
```

**Notes:**
- Database must exist before running the system
- User must have CREATE, INSERT, UPDATE, DELETE permissions
- Connection pooling is handled automatically (2-10 connections)

---

## 🧠 **LLM Integration Configuration**

### **OPENROUTER_API_KEY** (Required)
API key for OpenRouter service, providing access to multiple LLM providers.

```bash
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Getting Your Key:**
1. Sign up at [OpenRouter](https://openrouter.ai)
2. Navigate to API Keys section
3. Create a new API key
4. Add credits to your account

### **DEFAULT_MODEL** (Optional)
Primary LLM model for content generation tasks.

```bash
DEFAULT_MODEL=openai/gpt-3.5-turbo
```

**Recommended Models:**
- `openai/gpt-3.5-turbo` - Fast, cost-effective (default)
- `openai/gpt-4` - Higher quality, more expensive
- `anthropic/claude-3-haiku` - Good balance of speed/quality
- `anthropic/claude-3-sonnet` - High quality analysis

### **FALLBACK_MODEL** (Optional)
Backup model when primary model is unavailable.

```bash
FALLBACK_MODEL=anthropic/claude-3-haiku
```

### **ENABLE_LLM_FALLBACK** (Optional)
Enable fallback to keyword-based selection when LLM unavailable.

```bash
ENABLE_LLM_FALLBACK=true  # Default: true
```

---

## 🎨 **Image Generation Configuration**

### **FREEPIK_API_KEY** (Optional)
API key for Freepik Mystic image generation service.

```bash
FREEPIK_API_KEY=your-freepik-api-key-here
```

**Getting Your Key:**
1. Sign up at [Freepik API](https://freepik.com/api)
2. Subscribe to Mystic AI plan
3. Generate API key from dashboard
4. Add to your environment

**Without API Key:**
- System operates in "specification mode"
- Generates detailed prompts and parameters
- Ready for manual image generation

### **FREEPIK_WEBHOOK_URL** (Optional)
Webhook URL for async image generation notifications.

```bash
FREEPIK_WEBHOOK_URL=https://your-domain.com/webhook/freepik
```

**Use Cases:**
- Async processing for large batches
- Real-time status updates
- Integration with external systems

---

## 🎵 **Audio Generation Configuration**

### **ELEVEN_LABS_API_KEY** (Optional - Future)
API key for ElevenLabs voice generation service.

```bash
ELEVEN_LABS_API_KEY=your-elevenlabs-key-here
```

**Status:** Planned for future release
**Current:** Audio agents generate specifications only

---

## 🛠️ **System Configuration**

### **ASSETS_DIR** (Optional)
Directory for storing generated content assets.

```bash
ASSETS_DIR=./assets  # Default
ASSETS_DIR=/var/content-engine/assets  # Production
```

**Permissions:**
- Must be writable by application user
- Sufficient disk space for generated content
- Backup strategy recommended for production

### **TEMPLATES_DIR** (Optional)
Directory containing content template files.

```bash
TEMPLATES_DIR=./src/templates/markdown  # Default
TEMPLATES_DIR=/opt/content-engine/templates  # Production
```

**Requirements:**
- Must contain valid template files
- Readable by application user
- Version control recommended

### **LOG_LEVEL** (Optional)
Application logging verbosity level.

```bash
LOG_LEVEL=INFO  # Default
```

**Options:**
- `DEBUG` - Detailed debugging information
- `INFO` - General operational messages
- `WARNING` - Warning messages only
- `ERROR` - Error messages only

### **LOG_FILE** (Optional)
Log file path for persistent logging.

```bash
LOG_FILE=content_engine.log  # Default
LOG_FILE=/var/log/content-engine/app.log  # Production
```

**Notes:**
- Set to empty string for console-only logging
- Log rotation recommended for production
- Ensure directory is writable

### **DEBUG** (Optional)
Enable debug mode for development.

```bash
DEBUG=false  # Default
DEBUG=true   # Development
```

**Debug Mode Effects:**
- More verbose logging
- Detailed error messages
- Performance timing information
- Development-friendly error pages

---

## 🎯 **Environment-Specific Configurations**

### **Development Environment**
```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/content_engine_dev

# LLM Integration
OPENROUTER_API_KEY=sk-or-v1-dev-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo

# Image Generation (Optional)
FREEPIK_API_KEY=dev-freepik-key-here

# System
LOG_LEVEL=DEBUG
DEBUG=true
ASSETS_DIR=./assets
```

### **Production Environment**
```bash
# Database
DATABASE_URL=postgresql://user:secure_pass@prod-db.company.com:5432/content_engine

# LLM Integration
OPENROUTER_API_KEY=sk-or-v1-prod-key-here
DEFAULT_MODEL=openai/gpt-4
FALLBACK_MODEL=anthropic/claude-3-haiku

# Image Generation
FREEPIK_API_KEY=prod-freepik-key-here
FREEPIK_WEBHOOK_URL=https://api.company.com/webhook/freepik

# System
LOG_LEVEL=INFO
DEBUG=false
LOG_FILE=/var/log/content-engine/app.log
ASSETS_DIR=/var/content-engine/assets
```

### **Testing Environment**
```bash
# Database
DATABASE_URL=postgresql://test:test@localhost:5432/content_engine_test

# LLM Integration
OPENROUTER_API_KEY=sk-or-v1-test-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo

# System
LOG_LEVEL=WARNING
DEBUG=false
ENABLE_LLM_FALLBACK=false  # Test LLM integration specifically
```

---

## 🔒 **Security Best Practices**

### **API Key Management**
```bash
# ✅ Good: Environment variables
export OPENROUTER_API_KEY=sk-or-v1-your-key-here

# ✅ Good: .env file (not in version control)
echo "OPENROUTER_API_KEY=sk-or-v1-your-key-here" >> .env

# ❌ Bad: Hardcoded in source code
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"  # Never do this!
```

### **Database Security**
```bash
# ✅ Good: Strong password, specific user
DATABASE_URL=postgresql://content_engine:strong_random_password@host:5432/content_engine

# ❌ Bad: Default credentials, admin user
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

### **File Permissions**
```bash
# Secure .env file
chmod 600 .env

# Secure log directory
chmod 750 /var/log/content-engine/
chown content-engine:content-engine /var/log/content-engine/
```

---

## 🐳 **Docker Configuration**

### **Docker Compose Example**
```yaml
version: '3.8'
services:
  content-engine:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/content_engine
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - FREEPIK_API_KEY=${FREEPIK_API_KEY}
      - LOG_LEVEL=INFO
    depends_on:
      - db
    volumes:
      - ./assets:/app/assets
      - ./logs:/var/log/content-engine

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=content_engine
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Kubernetes ConfigMap**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: content-engine-config
data:
  LOG_LEVEL: "INFO"
  DEBUG: "false"
  ASSETS_DIR: "/app/assets"
  TEMPLATES_DIR: "/app/templates"
---
apiVersion: v1
kind: Secret
metadata:
  name: content-engine-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@host:5432/content_engine"
  OPENROUTER_API_KEY: "sk-or-v1-your-key-here"
  FREEPIK_API_KEY: "your-freepik-key-here"
```

---

## 🔍 **Configuration Validation**

### **Built-in Validation**
The system automatically validates configuration on startup:

```bash
python cli.py setup
```

**Validates:**
- Database connectivity and permissions
- API key format and accessibility
- Directory permissions and existence
- Template file validity

### **Manual Testing**
```bash
# Test LLM integration
python cli.py llm-test

# Test Freepik integration
python cli.py freepik-test

# Test complete system
python cli.py create "Test job" && python cli.py run <job-id>
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

**Database Connection Failed**
```bash
# Check connection string format
DATABASE_URL=postgresql://user:pass@host:port/database

# Test connection manually
psql postgresql://user:pass@host:port/database
```

**LLM API Errors**
```bash
# Verify API key format
echo $OPENROUTER_API_KEY | grep "sk-or-"

# Check account credits
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/auth/key
```

**Permission Errors**
```bash
# Check directory permissions
ls -la ./assets
ls -la /var/log/content-engine/

# Fix permissions
chmod 755 ./assets
chown -R app-user:app-group ./assets
```

### **Debug Mode**
Enable debug mode for detailed troubleshooting:

```bash
DEBUG=true LOG_LEVEL=DEBUG python cli.py create "test"
```

---

## 📊 **Configuration Templates**

### **Minimal Configuration**
```bash
# Required only
DATABASE_URL=postgresql://postgres:password@localhost:5432/content_engine
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### **Complete Configuration**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/content_engine

# LLM Integration
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEFAULT_MODEL=openai/gpt-3.5-turbo
FALLBACK_MODEL=anthropic/claude-3-haiku
ENABLE_LLM_FALLBACK=true

# Image Generation
FREEPIK_API_KEY=your-freepik-key-here
FREEPIK_WEBHOOK_URL=https://your-domain.com/webhook/freepik

# Audio Generation (Future)
ELEVEN_LABS_API_KEY=your-elevenlabs-key-here

# System Configuration
ASSETS_DIR=./assets
TEMPLATES_DIR=./src/templates/markdown
LOG_LEVEL=INFO
LOG_FILE=content_engine.log
DEBUG=false
```

---

**🔧 This configuration guide covers all aspects of Content Engine V2 setup, from basic requirements to production deployment strategies!**
