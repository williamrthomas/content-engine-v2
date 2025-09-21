"""Phase 2 integration tests for LLM-powered features"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from src.core.database import db_manager, init_database, close_database
from src.core.models import JobCreateRequest, JobStatus, TaskStatus
from src.engine.content_engine import ContentEngine
from src.llm.llm_service import LLMService
from src.llm.models import TemplateAnalysis, JobNaming
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
def content_engine():
    """Create a content engine instance"""
    return ContentEngine()


@pytest.fixture
def mock_template_analysis():
    """Mock template analysis response"""
    return TemplateAnalysis(
        content_type="blog",
        audience="professionals",
        tone="informative",
        complexity="intermediate",
        estimated_length="long",
        recommended_template="blog-post",
        confidence=0.9,
        reasoning="Content appears to be a comprehensive blog post about a technical topic"
    )


@pytest.fixture
def mock_job_naming():
    """Mock job naming response"""
    return JobNaming(
        primary_name="AI Trends Analysis 2024",
        display_name="Comprehensive Analysis of AI Trends in 2024",
        slug="ai-trends-analysis-2024",
        alternatives=["AI Technology Trends 2024", "2024 AI Industry Analysis"],
        seo_keywords=["AI", "trends", "2024", "analysis", "technology"],
        reasoning="SEO-optimized name focusing on key topic and year"
    )


@pytest.mark.asyncio
async def test_llm_service_initialization():
    """Test LLM service can be initialized"""
    try:
        async with LLMService() as llm_service:
            assert llm_service is not None
            assert llm_service.client is not None
    except ValueError as e:
        # Expected if API key is not configured
        assert "API key" in str(e)
    except Exception as e:
        pytest.fail(f"Unexpected error initializing LLM service: {e}")


@pytest.mark.asyncio
async def test_intelligent_template_selection_with_mock(content_engine, mock_template_analysis):
    """Test intelligent template selection with mocked LLM response"""
    
    with patch('src.engine.content_engine.LLMService') as mock_llm_service:
        # Setup mock
        mock_service_instance = AsyncMock()
        mock_service_instance.test_connection.return_value = True
        mock_service_instance.analyze_for_template_selection.return_value = mock_template_analysis
        mock_llm_service.return_value.__aenter__.return_value = mock_service_instance
        
        # Load templates
        await template_loader.load_all_templates()
        
        # Test intelligent selection
        template, analysis = await content_engine._intelligent_template_selection(
            "Write a comprehensive blog post about AI trends"
        )
        
        assert template is not None
        assert template.name == "blog-post"
        assert analysis.confidence == 0.9
        assert analysis.recommended_template == "blog-post"


@pytest.mark.asyncio
async def test_intelligent_template_selection_fallback(content_engine):
    """Test template selection falls back when LLM is unavailable"""
    
    with patch('src.engine.content_engine.LLMService') as mock_llm_service:
        # Setup mock to simulate LLM unavailability
        mock_service_instance = AsyncMock()
        mock_service_instance.test_connection.return_value = False
        mock_llm_service.return_value.__aenter__.return_value = mock_service_instance
        
        # Load templates
        await template_loader.load_all_templates()
        
        # Test fallback selection
        template, analysis = await content_engine._intelligent_template_selection(
            "Create a YouTube tutorial about Python"
        )
        
        assert template is not None
        assert analysis.confidence == 0.6  # Fallback confidence
        assert "Fallback" in analysis.reasoning


@pytest.mark.asyncio
async def test_intelligent_job_naming_with_mock(content_engine, mock_job_naming):
    """Test intelligent job naming with mocked LLM response"""
    
    with patch('src.engine.content_engine.LLMService') as mock_llm_service:
        # Setup mock
        mock_service_instance = AsyncMock()
        mock_service_instance.test_connection.return_value = True
        mock_service_instance.generate_job_name.return_value = mock_job_naming
        mock_llm_service.return_value.__aenter__.return_value = mock_service_instance
        
        # Create mock template
        mock_template = MagicMock()
        mock_template.name = "blog-post"
        
        request = JobCreateRequest(user_request="Write about AI trends")
        
        # Test intelligent naming
        names = await content_engine._generate_job_names(request, mock_template)
        
        assert names['technical_name'] == "ai-trends-analysis-2024"
        assert names['display_name'] == "Comprehensive Analysis of AI Trends in 2024"


@pytest.mark.asyncio
async def test_job_naming_fallback(content_engine):
    """Test job naming falls back when LLM is unavailable"""
    
    with patch('src.engine.content_engine.LLMService') as mock_llm_service:
        # Setup mock to simulate LLM unavailability
        mock_service_instance = AsyncMock()
        mock_service_instance.test_connection.return_value = False
        mock_llm_service.return_value.__aenter__.return_value = mock_service_instance
        
        request = JobCreateRequest(user_request="Write about sustainable energy")
        
        # Test fallback naming
        names = await content_engine._generate_job_names(request, None)
        
        assert "job-" in names['technical_name']
        assert "sustainable" in names['technical_name'] or "energy" in names['technical_name']
        assert names['display_name'] == "Write about sustainable energy"


@pytest.mark.asyncio
async def test_end_to_end_job_creation_with_llm_mock(content_engine, mock_template_analysis, mock_job_naming):
    """Test complete job creation workflow with mocked LLM responses"""
    
    with patch('src.engine.content_engine.LLMService') as mock_llm_service:
        # Setup mock
        mock_service_instance = AsyncMock()
        mock_service_instance.test_connection.return_value = True
        mock_service_instance.analyze_for_template_selection.return_value = mock_template_analysis
        mock_service_instance.generate_job_name.return_value = mock_job_naming
        mock_llm_service.return_value.__aenter__.return_value = mock_service_instance
        
        # Create job without specifying template (should use LLM)
        request = JobCreateRequest(
            user_request="Write a comprehensive blog post about AI trends in 2024"
        )
        
        job_response = await content_engine.create_job(request)
        
        # Verify job was created with LLM intelligence
        assert job_response.job.id is not None
        assert job_response.job.template_name == "blog-post"
        assert job_response.job.display_name == "Comprehensive Analysis of AI Trends in 2024"
        assert len(job_response.tasks) > 0


@pytest.mark.asyncio
async def test_fallback_template_selection_keywords(content_engine):
    """Test keyword-based fallback template selection"""
    
    # Load templates
    await template_loader.load_all_templates()
    
    # Test blog keywords
    template, analysis = await content_engine._select_template_fallback("Write a blog article about technology")
    assert template.name == "blog-post"
    
    # Test tutorial keywords
    template, analysis = await content_engine._select_template_fallback("Create a YouTube tutorial about coding")
    assert template.name == "youtube-tutorial"
    
    # Test default fallback
    template, analysis = await content_engine._select_template_fallback("Some random content request")
    assert template is not None  # Should get first available template


@pytest.mark.asyncio
async def test_job_creation_with_specified_template(content_engine):
    """Test that specified templates bypass LLM selection"""
    
    request = JobCreateRequest(
        user_request="Create some content",
        template_name="youtube-tutorial"
    )
    
    job_response = await content_engine.create_job(request)
    
    # Should use specified template regardless of content
    assert job_response.job.template_name == "youtube-tutorial"
    assert len(job_response.tasks) > 0


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
