# Content Engine V2 - Quick Start Guide

## 🚀 **Get Started in 5 Minutes**

Content Engine V2 is a production-ready system that transforms your ideas into professional content with real image generation.

---

## ⚡ **Instant Setup**

### **1. Prerequisites**
```bash
# Required
- Python 3.9+
- PostgreSQL database
- OpenRouter API key

# Optional (for real image generation)
- Freepik API key
```

### **2. Installation**
```bash
# Clone and setup
git clone <repository-url>
cd content-engine-v2-claude
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and database URL
```

### **3. Initialize System**
```bash
python cli.py setup
```

---

## 🎯 **Essential Commands**

### **Create Content**
```bash
# Let AI choose the best template
python cli.py create "Write a blog post about sustainable energy"
python cli.py create "Create daily top 5 AI news with thumbnails"
python cli.py create "Make a Docker tutorial for beginners"
```

### **Execute Jobs**
```bash
# Run a job (generates real content)
python cli.py run <job-id>

# Check status and results
python cli.py status <job-id>

# List all jobs
python cli.py list
```

### **Test Integrations**
```bash
# Test LLM integration
python cli.py llm-test

# Test image generation (if API key configured)
python cli.py freepik-test

# View available templates
python cli.py templates
```

---

## 🎨 **What You Get**

### **With Basic Setup (OpenRouter only)**
- **Research-backed content** with X post analysis
- **Professional writing** with SEO optimization
- **Detailed specifications** for images, audio, and video
- **Complete project outlines** ready for execution

### **With Freepik API (Real Generation)**
- **Professional images** at 2K/4K resolution
- **YouTube thumbnails** optimized for clicks
- **Social media graphics** with consistent branding
- **List graphics** with ranking numbers and styling

---

## 📊 **Example Workflow**

```bash
# 1. Create a job
$ python cli.py create "Daily AI news with professional thumbnails"
✓ Job created: c637921e-6a4a-4808-80aa-71561ba96304
Template: top-x-daily-list 🧠 (LLM selected)

# 2. Execute the job
$ python cli.py run c637921e-6a4a-4808-80aa-71561ba96304
✅ Research Agent: source_x_posts (score: 0.97)
✅ Writing Agent: write_full_script (score: 0.85)
✅ Freepik Mystic Agent: design_thumbnail (real image generated) ⭐

# 3. Check results
$ python cli.py status c637921e-6a4a-4808-80aa-71561ba96304
✓ Job completed successfully! 🎉
Professional images created: 3 files
Quality score: 0.82 (excellent)
```

---

## 🔧 **Configuration**

### **Required Environment Variables**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/content_engine

# LLM Integration
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### **Optional for Real Image Generation**
```bash
# Image Generation
FREEPIK_API_KEY=your-freepik-key-here
```

---

## 🎯 **Content Types**

### **Blog Posts** (`blog-post` template)
- Research-backed articles with expert insights
- SEO-optimized structure and headlines
- Professional infographics and social assets
- Complete content marketing package

### **Daily Lists** (`top-x-daily-list` template)
- Trending topic analysis with X post sourcing
- Professional YouTube thumbnails (real images)
- Consistent visual series for list items
- Social media promotion assets

### **Tutorials** (`youtube-tutorial` template)
- Step-by-step educational content
- Visual guides and diagrams
- Interactive elements and exercises
- Comprehensive resource lists

---

## 🚨 **Troubleshooting**

### **Common Issues**

**"Database connection failed"**
```bash
# Check your DATABASE_URL format
DATABASE_URL=postgresql://user:password@host:port/database
```

**"LLM test failed"**
```bash
# Verify your OpenRouter API key
echo $OPENROUTER_API_KEY | grep "sk-or-"
```

**"No images generated"**
```bash
# Check if Freepik API key is configured
python cli.py freepik-test
```

### **Get Help**
```bash
# Comprehensive help
python cli.py help

# Command-specific help
python cli.py create --help
python cli.py run --help
```

---

## 📚 **Next Steps**

### **Learn More**
- **[Complete Documentation](docs/README.md)** - Full feature guide
- **[CLI Reference](docs/cli-reference.md)** - All commands explained
- **[Examples Guide](docs/examples-and-usage.md)** - Real-world usage scenarios
- **[Configuration Guide](docs/configuration.md)** - Advanced setup options

### **Advanced Features**
- **Template Customization** - Create your own content templates
- **Agent Configuration** - Customize agent behavior and selection
- **API Integration** - Add new external services
- **Batch Processing** - Handle multiple jobs efficiently

---

## 🎉 **Success Indicators**

### **You're Ready When:**
✅ `python cli.py setup` completes successfully  
✅ `python cli.py llm-test` shows "Connected"  
✅ `python cli.py create "test"` generates a job  
✅ `python cli.py run <job-id>` executes without errors  

### **Bonus: Real Image Generation**
✅ `python cli.py freepik-test` shows "API integration ready!"  
✅ Image tasks show "real images generated" during execution  
✅ Professional images appear in your assets directory  

---

## 🚀 **Ready to Create?**

**Start with a simple command:**
```bash
python cli.py create "Write about the future of AI in healthcare"
```

**Then execute it:**
```bash
python cli.py run <job-id>
```

**🎉 You're now creating professional content with AI!**

---

*For detailed documentation, examples, and advanced features, see the [complete documentation](docs/README.md).*
