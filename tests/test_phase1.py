"""Phase 1 integration tests for Content Engine V2"""

import pytest
import asyncio
from uuid import uuid4

from src.core.database import db_manager, init_database, close_database
from src.core.models import JobCreateRequest, JobStatus, TaskStatus
from src.engine.content_engine import ContentEngine
from src.templates.loader import template_loader


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup database for testing"""
    await init_database()
    yield
    await close_database()


@pytest.fixture
async def content_engine():
    """Create a content engine instance"""
    return ContentEngine()


@pytest.mark.asyncio
async def test_template_loading():
    """Test that templates can be loaded successfully"""
    templates = await template_loader.load_all_templates()
    
    assert len(templates) > 0, "Should load at least one template"
    assert "blog-post" in templates, "Should load blog-post template"
    
    blog_template = templates["blog-post"]
    assert blog_template.name == "blog-post"
    assert len(blog_template.tasks) > 0, "Template should have tasks"
    
    # Check that tasks are properly categorized
    categories = set(task.category for task in blog_template.tasks)
    assert "script" in categories, "Should have script tasks"


@pytest.mark.asyncio
async def test_job_creation(content_engine):
    """Test job creation with template selection"""
    request = JobCreateRequest(
        user_request="Create a blog post about sustainable energy solutions",
        template_name="blog-post"
    )
    
    job_response = await content_engine.create_job(request)
    
    # Verify job was created
    assert job_response.job.id is not None
    assert job_response.job.name.startswith("job-")
    assert job_response.job.display_name == request.user_request
    assert job_response.job.template_name == "blog-post"
    assert job_response.job.status == JobStatus.PENDING
    
    # Verify tasks were created
    assert len(job_response.tasks) > 0, "Should create tasks from template"
    
    # Verify task categories are present
    task_categories = set(task.category for task in job_response.tasks)
    assert "script" in task_categories, "Should have script tasks"
    
    # Verify tasks have proper sequence order
    script_tasks = [t for t in job_response.tasks if t.category == "script"]
    sequence_orders = [t.sequence_order for t in script_tasks]
    assert sequence_orders == sorted(sequence_orders), "Tasks should be in sequence order"


@pytest.mark.asyncio
async def test_job_processing(content_engine):
    """Test complete job processing workflow"""
    # Create a job
    request = JobCreateRequest(
        user_request="Write a short blog post about AI trends",
        template_name="blog-post"
    )
    
    job_response = await content_engine.create_job(request)
    job_id = job_response.job.id
    
    # Process the job
    success = await content_engine.process_job(job_id)
    assert success, "Job processing should succeed"
    
    # Check final job status
    final_response = await content_engine.get_job_status(job_id)
    assert final_response is not None
    assert final_response.job.status == JobStatus.COMPLETED
    
    # Check that all tasks were completed
    completed_tasks = [t for t in final_response.tasks if t.status == TaskStatus.COMPLETED]
    assert len(completed_tasks) == len(final_response.tasks), "All tasks should be completed"
    
    # Verify tasks have outputs
    for task in completed_tasks:
        assert task.parameters.get("outputs"), f"Task {task.task_name} should have outputs"


@pytest.mark.asyncio
async def test_auto_template_selection(content_engine):
    """Test automatic template selection based on request content"""
    # Test blog post detection
    blog_request = JobCreateRequest(
        user_request="I want to write a blog article about machine learning"
    )
    
    job_response = await content_engine.create_job(blog_request)
    assert job_response.job.template_name == "blog-post"
    
    # Test video tutorial detection
    video_request = JobCreateRequest(
        user_request="Create a YouTube tutorial about Python programming"
    )
    
    job_response = await content_engine.create_job(video_request)
    assert job_response.job.template_name == "youtube-tutorial"


@pytest.mark.asyncio
async def test_job_status_retrieval(content_engine):
    """Test job status retrieval"""
    # Create a job
    request = JobCreateRequest(
        user_request="Test job for status retrieval"
    )
    
    job_response = await content_engine.create_job(request)
    job_id = job_response.job.id
    
    # Retrieve status
    status_response = await content_engine.get_job_status(job_id)
    assert status_response is not None
    assert status_response.job.id == job_id
    assert len(status_response.tasks) > 0


@pytest.mark.asyncio
async def test_system_stats(content_engine):
    """Test system statistics retrieval"""
    stats = await content_engine.get_system_stats()
    
    assert "total_jobs" in stats
    assert "database_connected" in stats
    assert "templates_loaded" in stats
    assert stats["database_connected"] is True
    assert stats["templates_loaded"] > 0


@pytest.mark.asyncio
async def test_database_health():
    """Test database health check"""
    is_healthy = await db_manager.health_check()
    assert is_healthy, "Database should be healthy"


@pytest.mark.asyncio
async def test_job_listing(content_engine):
    """Test job listing functionality"""
    # Create a few jobs
    for i in range(3):
        request = JobCreateRequest(
            user_request=f"Test job {i} for listing"
        )
        await content_engine.create_job(request)
    
    # List all jobs
    jobs = await content_engine.list_jobs(limit=10)
    assert len(jobs) >= 3, "Should return at least the jobs we created"
    
    # List pending jobs only
    pending_jobs = await content_engine.list_jobs(status=JobStatus.PENDING, limit=10)
    assert len(pending_jobs) >= 3, "Should return pending jobs"


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
