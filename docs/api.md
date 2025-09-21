# Content Engine V2 - API Reference

## Core Classes

### ContentEngine

Main orchestration class for content creation jobs.

```python
from src.engine.content_engine import ContentEngine

engine = ContentEngine()
```

#### Methods

##### `create_job(request: JobCreateRequest) -> JobResponse`
Creates a new content generation job.

**Parameters:**
- `request`: JobCreateRequest with user_request and optional template_name

**Returns:**
- JobResponse with created job and tasks

**Example:**
```python
request = JobCreateRequest(
    user_request="Write a blog post about AI",
    template_name="blog-post"
)
response = await engine.create_job(request)
```

##### `get_job_status(job_id: UUID) -> Optional[JobResponse]`
Retrieves job status with all tasks.

##### `process_job(job_id: UUID) -> bool`
Processes all tasks for a job sequentially.

##### `list_jobs(status: Optional[JobStatus] = None, limit: int = 50) -> List[Job]`
Lists jobs with optional filtering.

### TaskRunner

Handles sequential execution of tasks within jobs.

```python
from src.engine.task_runner import TaskRunner

runner = TaskRunner()
```

#### Methods

##### `process_job(job_id: UUID) -> bool`
Processes all tasks for a job in category order.

##### `register_agent(agent_key: str, agent: BaseAgent) -> None`
Registers an agent for task execution.

### BaseAgent

Abstract base class for all content generation agents.

```python
from src.agents.base_agent import BaseAgent
from src.core.models import Task, TaskResult, TaskCategory

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("My Agent", TaskCategory.SCRIPT)
    
    async def execute(self, task: Task) -> TaskResult:
        # Implementation here
        pass
    
    async def validate_task(self, task: Task) -> bool:
        return task.category == self.category
```

## Data Models

### Job

Represents a content creation job.

```python
from src.core.models import Job, JobStatus

job = Job(
    name="job-ai-blog-20240121-001",
    display_name="Blog Post: AI Trends 2024",
    template_name="blog-post",
    user_request="Write about AI trends",
    status=JobStatus.PENDING
)
```

**Fields:**
- `id`: UUID - Unique identifier
- `name`: str - Technical job name
- `display_name`: str - Human-readable name
- `template_name`: str - Template used
- `user_request`: str - Original request
- `status`: JobStatus - Current status
- `created_at`: datetime - Creation timestamp
- `completed_at`: datetime - Completion timestamp

### Task

Represents an individual task within a job.

```python
from src.core.models import Task, TaskCategory, TaskStatus

task = Task(
    job_id=job_id,
    task_name="write_article",
    category=TaskCategory.SCRIPT,
    sequence_order=1,
    status=TaskStatus.PENDING,
    parameters={
        "inputs": {"user_request": "Write about AI"},
        "requirements": {"word_count": 1200},
        "outputs": {}
    }
)
```

**Fields:**
- `id`: UUID - Unique identifier
- `job_id`: UUID - Parent job reference
- `task_name`: str - Task name from template
- `category`: TaskCategory - Task category
- `sequence_order`: int - Execution order
- `status`: TaskStatus - Current status
- `assigned_agent_id`: UUID - Assigned agent
- `parameters`: Dict - Task data (inputs, requirements, outputs)
- `started_at`: datetime - Start timestamp
- `completed_at`: datetime - Completion timestamp
- `error_message`: str - Error details if failed

### Agent

Represents a content generation agent.

```python
from src.core.models import Agent, TaskCategory, AgentStatus

agent = Agent(
    name="GPT-4 Script Writer",
    instance_key="gpt4_script_writer",
    category=TaskCategory.SCRIPT,
    provider="openai",
    model="gpt-4",
    specialization="Blog post and article writing",
    config={"api_key": "...", "temperature": 0.7},
    status=AgentStatus.ACTIVE
)
```

## Template System

### Template

Represents a content template.

```python
from src.core.models import Template, TemplateTask

template = Template(
    name="blog-post",
    title="Blog Post Article",
    description="Comprehensive blog post template",
    category="article",
    tasks=[...],
    metadata={"target_words": 1200}
)
```

### TemplateLoader

Loads and parses markdown templates.

```python
from src.templates.loader import template_loader

# Load all templates
templates = await template_loader.load_all_templates()

# Load specific template
template = await template_loader.load_template("blog-post")

# Get loaded template
template = template_loader.get_template("blog-post")
```

## Database Operations

### DatabaseManager

Manages PostgreSQL database connections and operations.

```python
from src.core.database import db_manager

# Job operations
job = await db_manager.create_job(job)
job = await db_manager.get_job(job_id)
jobs = await db_manager.get_jobs(status=JobStatus.PENDING)

# Task operations
task = await db_manager.create_task(task)
tasks = await db_manager.get_tasks_for_job(job_id)
next_task = await db_manager.get_next_pending_task(job_id)

# Agent operations
agent = await db_manager.create_agent(agent)
agents = await db_manager.get_agents_for_category(TaskCategory.SCRIPT)
```

## Configuration

### Settings

Application configuration with environment variable support.

```python
from src.core.config import settings

# Access configuration
database_url = settings.database_url
api_key = settings.openrouter_api_key
assets_dir = settings.assets_dir

# Helper functions
from src.core.config import get_database_url, get_openrouter_api_key

url = get_database_url()  # Validates and returns URL
key = get_openrouter_api_key()  # Validates and returns API key
```

## Enums

### JobStatus
- `PENDING` - Job created, not started
- `IN_PROGRESS` - Job currently processing
- `COMPLETED` - Job finished successfully
- `FAILED` - Job failed

### TaskStatus
- `PENDING` - Task waiting to execute
- `IN_PROGRESS` - Task currently running
- `COMPLETED` - Task finished successfully
- `FAILED` - Task execution failed

### TaskCategory
- `SCRIPT` - Text content generation
- `IMAGE` - Visual content generation
- `AUDIO` - Audio content generation
- `VIDEO` - Video content generation

### AgentStatus
- `ACTIVE` - Agent available for tasks
- `DISABLED` - Agent temporarily unavailable

## Error Handling

### Common Exceptions

```python
# Database connection errors
try:
    await db_manager.health_check()
except Exception as e:
    logger.error(f"Database error: {e}")

# Template loading errors
try:
    template = await template_loader.load_template("invalid")
except Exception as e:
    logger.error(f"Template error: {e}")

# Job processing errors
try:
    success = await engine.process_job(job_id)
except Exception as e:
    logger.error(f"Processing error: {e}")
```

## Usage Examples

### Complete Workflow

```python
import asyncio
from src.engine.content_engine import ContentEngine
from src.core.models import JobCreateRequest
from src.core.database import init_database, close_database

async def main():
    # Initialize system
    await init_database()
    
    # Create engine
    engine = ContentEngine()
    
    # Create job
    request = JobCreateRequest(
        user_request="Write a blog post about sustainable energy",
        template_name="blog-post"
    )
    
    job_response = await engine.create_job(request)
    print(f"Created job: {job_response.job.id}")
    
    # Process job
    success = await engine.process_job(job_response.job.id)
    print(f"Processing {'succeeded' if success else 'failed'}")
    
    # Check final status
    final_status = await engine.get_job_status(job_response.job.id)
    print(f"Final status: {final_status.job.status}")
    
    # Cleanup
    await close_database()

# Run the workflow
asyncio.run(main())
```

### Custom Agent Implementation

```python
from src.agents.base_agent import BaseAgent
from src.core.models import Task, TaskResult, TaskCategory, TaskStatus

class CustomScriptAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Custom Script Agent",
            category=TaskCategory.SCRIPT,
            config={"custom_param": "value"}
        )
    
    async def execute(self, task: Task) -> TaskResult:
        try:
            inputs = self._extract_task_inputs(task)
            requirements = self._extract_task_requirements(task)
            
            # Custom processing logic
            content = await self._generate_content(inputs, requirements)
            
            return self._create_success_result(
                task=task,
                outputs={"content": content, "word_count": len(content.split())},
                metadata={"agent": self.name}
            )
            
        except Exception as e:
            return self._create_error_result(task, str(e))
    
    async def validate_task(self, task: Task) -> bool:
        return (task.category == TaskCategory.SCRIPT and 
                "write" in task.task_name.lower())
    
    async def _generate_content(self, inputs, requirements):
        # Implementation here
        return "Generated content..."
```

This API reference covers the core functionality available in Phase 1 of Content Engine V2. The system is designed to be extensible, with clear interfaces for adding new agents, templates, and functionality in future phases.
