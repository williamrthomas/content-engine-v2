# Examples and Usage Guide

## 🚀 **Complete Usage Examples for Content Engine V2**

This guide provides comprehensive examples of using Content Engine V2 for various content creation scenarios, from simple blog posts to complex multimedia projects with real image generation.

## 📋 **Quick Start Examples**

### **1. Basic Blog Post Creation**
```bash
# Create a comprehensive blog post
python cli.py create "Write a detailed guide about sustainable energy solutions for homeowners"

# Output:
🧠 Using LLM intelligence for template selection...
✓ Job created successfully!
Job ID: 65eff2df-312e-46df-9413-d095e934a9ed
Template: blog-post 🧠 (LLM selected)
Display Name: Comprehensive Guide: Sustainable Energy Solutions for Homeowners
Tasks Created: 14 (7 script, 3 image, 2 audio, 2 video)

# Execute the job
python cli.py run 65eff2df-312e-46df-9413-d095e934a9ed
```

### **2. YouTube Content with Real Thumbnails**
```bash
# Create YouTube content with professional thumbnails
python cli.py create "Create daily top 5 AI breakthroughs with professional thumbnails"

# Output:
🧠 Using LLM intelligence for template selection...
✓ Job created successfully!
Job ID: c637921e-6a4a-4808-80aa-71561ba96304
Template: top-x-daily-list 🧠 (LLM selected)
Display Name: Daily Top 5 AI Breakthroughs with Professional Thumbnails
Tasks Created: 15 (7 script, 3 image, 2 audio, 3 video)

# Execute with real image generation
python cli.py run c637921e-6a4a-4808-80aa-71561ba96304

# Live execution output:
✅ Research Agent: source_x_posts (score: 0.97)
✅ Writing Agent: write_full_script (score: 0.85)
✅ Freepik Mystic Agent: design_thumbnail (template-specified) ⭐
✅ Freepik Mystic Agent: create_list_graphics (real images generated)
```

### **3. Educational Tutorial**
```bash
# Force specific template for educational content
python cli.py create "Docker containerization for beginners" --template youtube-tutorial

# Output:
✓ Job created successfully!
Job ID: 8a9b7c6d-5e4f-3210-9876-543210fedcba
Template: youtube-tutorial (manually selected)
Display Name: Docker Containerization Tutorial for Beginners
Tasks Created: 12 (5 script, 3 image, 2 audio, 2 video)
```

---

## 🎯 **Content Type Examples**

### **Blog Posts**
Perfect for comprehensive articles, guides, and thought leadership content.

```bash
# Technology guides
python cli.py create "Complete guide to machine learning for business leaders"
python cli.py create "Cybersecurity best practices for remote teams"
python cli.py create "The future of renewable energy technology"

# Industry analysis
python cli.py create "2024 trends in artificial intelligence and automation"
python cli.py create "Impact of blockchain on supply chain management"

# How-to guides
python cli.py create "How to implement DevOps practices in small teams"
python cli.py create "Building scalable web applications with microservices"
```

**Generated Content:**
- Research-backed articles with expert insights
- SEO-optimized headlines and structure
- Professional infographics and diagrams
- Social media promotion assets
- Audio narration specifications

### **Daily List Videos**
Ideal for trending topics, news roundups, and curated content.

```bash
# AI and technology
python cli.py create "Today's top 7 AI tool releases with analysis"
python cli.py create "Weekly roundup: biggest tech acquisitions"
python cli.py create "Top 5 cybersecurity threats this month"

# Business and finance
python cli.py create "Daily crypto market movers and analysis"
python cli.py create "Top 10 startup funding rounds this week"

# Industry-specific
python cli.py create "Latest healthcare technology breakthroughs"
python cli.py create "Green energy innovations making headlines"
```

**Generated Content:**
- Professional YouTube thumbnails (real images via Freepik)
- Consistent visual series for list items
- Research-backed content with trending analysis
- Social media teasers and promotional graphics
- Platform-optimized video specifications

### **Educational Tutorials**
Best for step-by-step guides, technical tutorials, and learning content.

```bash
# Programming tutorials
python cli.py create "Python web development with FastAPI" --template youtube-tutorial
python cli.py create "React hooks explained with practical examples"
python cli.py create "Database design principles for beginners"

# Business skills
python cli.py create "Project management fundamentals for new managers"
python cli.py create "Digital marketing strategies for small businesses"

# Creative skills
python cli.py create "Video editing techniques for content creators"
python cli.py create "Graphic design principles for non-designers"
```

**Generated Content:**
- Structured learning modules with clear objectives
- Step-by-step visual guides and diagrams
- Interactive elements and practice exercises
- Professional presentation materials
- Comprehensive resource lists and references

---

## 🔧 **System Testing Examples**

### **Integration Testing**
```bash
# Test all system integrations
python cli.py setup
python cli.py llm-test
python cli.py freepik-test

# Expected output for working system:
🚀 Content Engine V2 Setup
✅ Database connection established
✅ Schema created successfully
✅ Agent registry initialized (7 agents)

🧠 Testing LLM Integration...
✅ LLM Service Status: Connected
🎉 Phase 2+ features are fully operational!

🎨 Testing Freepik Integration...
✅ Freepik Agent: Freepik Mystic Agent
✅ API Key Configured: True
🎉 Freepik API integration ready!
```

### **Template Testing**
```bash
# View available templates
python cli.py templates

# Output:
📋 Available Templates
┌─────────────────┬─────────────────────────────────┬───────┬──────────────────────┐
│ Template        │ Description                     │ Tasks │ Agent Assignments    │
├─────────────────┼─────────────────────────────────┼───────┼──────────────────────┤
│ blog-post       │ Comprehensive blog articles     │ 14    │ Research + Writing   │
│ top-x-daily-list│ Daily list videos with images   │ 15    │ Research + Freepik   │
│ youtube-tutorial│ Educational video content       │ 12    │ Writing + Design     │
└─────────────────┴─────────────────────────────────┴───────┴──────────────────────┘
```

### **Job Management Examples**
```bash
# List recent jobs
python cli.py list

# Check specific job status
python cli.py status c637921e-6a4a-4808-80aa-71561ba96304

# Filter jobs by status
python cli.py list --status completed
python cli.py list --status running --limit 5
```

---

## 🎨 **Real Image Generation Examples**

### **With Freepik API Key**
When FREEPIK_API_KEY is configured, the system generates actual professional images:

```bash
# Create content with real image generation
python cli.py create "Professional YouTube thumbnail for AI news channel"

# Execution shows real generation:
✅ Freepik Mystic Agent: design_thumbnail (template-specified)
   → Generated: professional_ai_news_thumbnail_1280x720.jpg
   → Quality: 4K resolution, optimized for mobile viewing
   → Style: Bold, high-contrast, AI-themed visual elements

✅ Freepik Mystic Agent: create_list_graphics (real images generated)
   → Generated: ai_news_card_01.jpg, ai_news_card_02.jpg, ...
   → Series: Consistent branding, ranking numbers, professional quality
```

### **Without API Key (Specification Mode)**
Without API keys, the system creates detailed specifications for manual generation:

```bash
# Same command without API key
python cli.py create "Professional YouTube thumbnail for AI news channel"

# Execution shows specification generation:
✅ Design Agent: design_thumbnail (specifications)
   → Prompt: "Create a bold, eye-catching YouTube thumbnail featuring..."
   → Specifications: 1280x720, high contrast, mobile-optimized
   → Color scheme: Blue/white tech theme with accent colors
   → Typography: Bold sans-serif, readable at small sizes
```

---

## 📊 **Production Workflow Examples**

### **Daily Content Creation**
```bash
#!/bin/bash
# Daily content automation script

# Create daily AI news
JOB1=$(python cli.py create "Daily top 5 AI breakthroughs with analysis" --format id)

# Create weekly roundup
JOB2=$(python cli.py create "Weekly tech trends and market analysis" --format id)

# Execute jobs
python cli.py run $JOB1
python cli.py run $JOB2

# Check results
python cli.py status $JOB1
python cli.py status $JOB2

# Generate summary report
python cli.py list --status completed --limit 10
```

### **Batch Processing**
```bash
# Create multiple jobs for a content series
python cli.py create "Machine Learning Basics: Introduction and Overview"
python cli.py create "Machine Learning Basics: Data Preprocessing Techniques"
python cli.py create "Machine Learning Basics: Model Selection and Training"
python cli.py create "Machine Learning Basics: Evaluation and Optimization"

# Process all pending jobs
for job_id in $(python cli.py list --status pending --format ids); do
    echo "Processing job: $job_id"
    python cli.py run $job_id
    python cli.py status $job_id
done
```

### **Quality Monitoring**
```bash
# Monitor job quality and performance
python cli.py list --status completed | grep "Quality:"

# Check agent performance
python cli.py status <job-id> | grep "Agent Performance"

# Review cost and usage
python cli.py llm-test | grep "Usage Statistics"
```

---

## 🎯 **Advanced Usage Patterns**

### **Custom Template Selection**
```bash
# Let LLM choose (recommended)
python cli.py create "Create engaging content about space exploration"

# Force specific template when needed
python cli.py create "Space exploration guide" --template blog-post
python cli.py create "Space news updates" --template top-x-daily-list
python cli.py create "Space science tutorial" --template youtube-tutorial
```

### **Environment-Specific Usage**
```bash
# Development environment
DEBUG=true LOG_LEVEL=DEBUG python cli.py create "Test content"

# Production environment
LOG_LEVEL=INFO python cli.py run <job-id>

# Testing with specific APIs
FREEPIK_API_KEY=test-key python cli.py freepik-test
```

### **Integration with External Systems**
```bash
# Webhook integration for async processing
export FREEPIK_WEBHOOK_URL=https://your-system.com/webhook/freepik

# Custom asset directory
export ASSETS_DIR=/var/content-engine/assets

# Custom logging
export LOG_FILE=/var/log/content-engine/production.log
```

---

## 🚨 **Troubleshooting Examples**

### **Common Issues and Solutions**

**LLM Integration Issues:**
```bash
# Test LLM connectivity
python cli.py llm-test

# Check API key format
echo $OPENROUTER_API_KEY | grep "sk-or-"

# Verify account credits
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/auth/key
```

**Database Connection Issues:**
```bash
# Test database connectivity
python cli.py setup

# Check connection string
echo $DATABASE_URL

# Manual connection test
psql $DATABASE_URL -c "SELECT version();"
```

**Image Generation Issues:**
```bash
# Test Freepik integration
python cli.py freepik-test

# Check API key configuration
echo $FREEPIK_API_KEY | wc -c  # Should be > 20 characters

# Verify agent selection
python cli.py create "test image" && python cli.py run <job-id>
```

### **Debug Mode Examples**
```bash
# Enable comprehensive debugging
DEBUG=true LOG_LEVEL=DEBUG python cli.py create "debug test"

# Monitor job execution in detail
DEBUG=true python cli.py run <job-id>

# Check agent selection logic
DEBUG=true python cli.py status <job-id>
```

---

## 📈 **Performance Examples**

### **Benchmarking**
```bash
# Time job creation
time python cli.py create "Performance test content"

# Monitor execution performance
time python cli.py run <job-id>

# Check system statistics
python cli.py llm-test | grep "Usage Statistics"
```

### **Cost Optimization**
```bash
# Use cost-effective models
DEFAULT_MODEL=openai/gpt-3.5-turbo python cli.py create "Cost-optimized content"

# Monitor token usage
python cli.py llm-test | grep "Total tokens"

# Batch similar requests
python cli.py create "Batch request 1: AI news"
python cli.py create "Batch request 2: AI news"
python cli.py create "Batch request 3: AI news"
```

---

## 🎉 **Success Metrics Examples**

### **Quality Metrics**
```bash
# Check agent performance scores
python cli.py status <job-id> | grep "score:"

# Review quality ratings
python cli.py list | grep "Quality:"

# Monitor success rates
python cli.py list --status completed | wc -l
python cli.py list --status failed | wc -l
```

### **Production Metrics**
```bash
# Daily content generation stats
python cli.py list --status completed | grep "$(date +%Y-%m-%d)" | wc -l

# Agent utilization
python cli.py status <job-id> | grep "Agent Performance"

# Cost per job
python cli.py llm-test | grep "Estimated cost"
```

---

## 🚀 **Real-World Use Cases**

### **Content Marketing Agency**
```bash
# Client 1: Tech startup blog content
python cli.py create "AI startup funding trends and market analysis"
python cli.py create "SaaS product launch strategy guide"

# Client 2: Educational YouTube channel
python cli.py create "Daily tech news roundup with professional graphics"
python cli.py create "Programming tutorial: Building REST APIs"

# Client 3: Social media content
python cli.py create "Weekly social media content calendar for tech brands"
```

### **News and Media Organization**
```bash
# Daily news production
python cli.py create "Breaking: Latest developments in renewable energy policy"
python cli.py create "Market analysis: Tech stock performance this week"
python cli.py create "Interview recap: CEO insights on AI industry trends"

# Video content with thumbnails
python cli.py create "Today's top 5 business news stories with analysis"
python cli.py create "Weekly roundup: Global economic indicators"
```

### **Educational Institution**
```bash
# Course content creation
python cli.py create "Introduction to Data Science: Course Module 1"
python cli.py create "Advanced Python Programming: Web Development Track"
python cli.py create "Digital Marketing Fundamentals: Social Media Strategy"

# Research and analysis
python cli.py create "Current trends in online education technology"
python cli.py create "Student engagement strategies for remote learning"
```

---

**🎯 This comprehensive guide covers every aspect of using Content Engine V2, from basic content creation to advanced production workflows with real asset generation!**

**Ready to create professional content at scale? Start with `python cli.py setup` and explore these examples!** 🚀
