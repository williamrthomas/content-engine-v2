"""Main Content Engine V2 - Professional Content Creation Engine

The core orchestration engine that transforms user requests into professional-quality
content across all media types. Combines LLM intelligence with specialized agents
and real API integrations for complete content generation workflows.

Key Features:
- LLM-powered template selection and job naming
- Template-driven agent assignment for deterministic workflows  
- Real content generation via API integrations (Freepik, etc.)
- Quality assurance with validation and scoring systems
- Production-scale processing with comprehensive error handling

Architecture:
- ContentEngine: Main orchestration class
- LLM Integration: OpenRouter API for intelligent decision making
- Agent Registry: Manages specialized content generation agents
- Task Runner: Executes sequential content creation workflows
- Database: PostgreSQL with comprehensive job and task tracking

Author: Content Engine V2 Team
Version: Phase 3+ Complete - Real Content Generation
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from ..core.database import db_manager
from ..core.models import Job, Task, JobCreateRequest, JobResponse, JobStatus, TaskStatus
from ..templates.loader import template_loader
from ..llm.llm_service import LLMService
from .task_runner import TaskRunner

logger = logging.getLogger(__name__)


class ContentEngine:
    """Main orchestration class for content creation jobs"""
    
    def __init__(self):
        self.task_runner = TaskRunner()
    
    async def create_job(self, request: JobCreateRequest) -> JobResponse:
        """Create a new content generation job with LLM intelligence"""
        
        logger.info(f"Creating job for request: {request.user_request}...")
        
        # Load templates
        await template_loader.load_all_templates()
        
        # Select template using LLM intelligence or fallback
        if request.template_name:
            template = template_loader.get_template(request.template_name)
            if not template:
                raise ValueError(f"Template '{request.template_name}' not found")
            logger.info(f"Using specified template: {request.template_name}")
            template_analysis = None
        else:
            # Use LLM for intelligent template selection
            template, template_analysis = await self._intelligent_template_selection(request.user_request)
            logger.info(f"LLM selected {template.name} template (confidence: {template_analysis.confidence:.2f})")
        
        # Generate job names (Phase 2 will use LLM)
        job_names = await self._generate_job_names(request, template)
        
        # Create job record
        job = Job(
            name=job_names['technical_name'],
            display_name=job_names['display_name'],
            template_name=template.name if template else None,
            user_request=request.user_request,
            status=JobStatus.PENDING
        )
        
        # Save job to database
        created_job = await db_manager.create_job(job)
        logger.info(f"Created job {created_job.id} with name {created_job.name}")
        
        # Create tasks from template
        tasks = []
        if template:
            tasks = await self._create_tasks_from_template(created_job.id, template, request)
            logger.info(f"Created {len(tasks)} tasks for job {created_job.id}")
        
        return JobResponse(job=created_job, tasks=tasks)
    
    async def get_job_status(self, job_id: UUID) -> Optional[JobResponse]:
        """Get job status with tasks"""
        job = await db_manager.get_job_by_id(job_id)
        if not job:
            return None
        
        tasks = await db_manager.get_tasks_for_job(job_id)
        return JobResponse(job=job, tasks=tasks)
    
    async def process_job(self, job_id: UUID) -> bool:
        """Process all tasks for a job sequentially"""
        logger.info(f"Starting job processing for {job_id}")
        
        try:
            # Update job status to in_progress
            await db_manager.update_job_status(job_id, JobStatus.IN_PROGRESS)
            
            # Process job using task runner
            success = await self.task_runner.process_job(job_id)
            
            # Update final job status
            final_status = JobStatus.COMPLETED if success else JobStatus.FAILED
            completed_at = datetime.utcnow() if success else None
            await db_manager.update_job_status(job_id, final_status, completed_at)
            
            logger.info(f"Job {job_id} processing completed with status: {final_status}")
            return success
            
        except Exception as e:
            logger.error(f"Job processing failed for {job_id}: {e}")
            await db_manager.update_job_status(job_id, JobStatus.FAILED)
            return False
    
    async def list_jobs(self, status: Optional[JobStatus] = None, limit: int = 50) -> List[Job]:
        """List jobs with optional filtering"""
        return await db_manager.get_jobs(status=status, limit=limit)
    
    # Private methods for job creation
    
    async def _intelligent_template_selection(self, user_request: str):
        """Use LLM for intelligent template selection"""
        try:
            async with LLMService() as llm_service:
                # Test connection first
                if not await llm_service.test_connection():
                    logger.warning("LLM service unavailable, using fallback selection")
                    return await self._select_template_fallback(user_request)
                
                # Get LLM analysis
                analysis = await llm_service.analyze_for_template_selection(user_request)
                template = template_loader.get_template(analysis.recommended_template)
                
                if template:
                    logger.info(f"LLM selected template: {analysis.recommended_template} (confidence: {analysis.confidence:.2f})")
                    return template, analysis
                else:
                    logger.warning(f"LLM recommended invalid template: {analysis.recommended_template}")
                    return await self._select_template_fallback(user_request)
                    
        except Exception as e:
            logger.error(f"LLM template selection failed: {e}")
            return await self._select_template_fallback(user_request)
    
    async def _select_template_fallback(self, user_request: str):
        """Fallback template selection using keywords"""
        
        templates = template_loader.list_templates()
        if not templates:
            raise ValueError("No templates available")
        
        request_lower = user_request.lower()
        
        # Simple keyword matching
        if any(word in request_lower for word in ["tutorial", "video", "youtube", "teach", "guide", "how to"]):
            template_name = "youtube-tutorial" if "youtube-tutorial" in templates else templates[0]
        elif any(word in request_lower for word in ["blog", "article", "post", "write"]):
            template_name = "blog-post" if "blog-post" in templates else templates[0]
        else:
            template_name = templates[0]  # Default to first available
        
        template = template_loader.get_template(template_name)
        
        # Create a simple analysis for the fallback
        from ..llm.models import TemplateAnalysis
        fallback_analysis = TemplateAnalysis(
            content_type="general",
            audience="general", 
            tone="informative",
            complexity="intermediate",
            estimated_length="medium",
            recommended_template=template.name,
            confidence=0.6,
            reasoning="Fallback keyword-based selection due to LLM unavailability"
        )
        
        return template, fallback_analysis
    
    async def _generate_job_names(self, request: JobCreateRequest, template: Optional[object]) -> Dict[str, str]:
        """Generate technical and display names for the job using LLM intelligence"""
        
        try:
            async with LLMService() as llm_service:
                # Test connection first
                if await llm_service.test_connection():
                    # Use LLM for intelligent naming
                    template_name = template.name if template else "general"
                    job_naming = await llm_service.generate_job_name(request.user_request, template_name)
                    
                    logger.info(f"LLM generated job name: {job_naming.primary_name}")
                    
                    return {
                        'technical_name': job_naming.slug,
                        'display_name': job_naming.display_name
                    }
                else:
                    logger.warning("LLM service unavailable, using fallback naming")
                    
        except Exception as e:
            logger.error(f"LLM job naming failed: {e}")
        
        # Fallback to simple naming
        return self._generate_job_names_fallback(request)
    
    def _generate_job_names_fallback(self, request: JobCreateRequest) -> Dict[str, str]:
        """Fallback job naming strategy"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        # Extract key words from request for technical name
        words = request.user_request.lower().split()
        key_words = [w for w in words[:3] if len(w) > 3 and w.isalpha()]
        
        if key_words:
            technical_name = f"job-{'-'.join(key_words)}-{timestamp}"
        else:
            technical_name = f"job-content-{timestamp}"
        
        # Create display name
        display_name = request.user_request[:60]
        if len(request.user_request) > 60:
            display_name += "..."
        
        return {
            'technical_name': technical_name,
            'display_name': display_name
        }
    
    async def _create_tasks_from_template(self, job_id: UUID, template: object, request: JobCreateRequest) -> List[Task]:
        """Create task records from template definition"""
        tasks = []
        
        for template_task in template.tasks:
            # Create task with parameters populated from template and request
            task_parameters = {
                'inputs': {
                    'user_request': request.user_request,
                    'template_name': template.name,
                    'job_id': str(job_id)
                },
                'requirements': template_task.parameters.copy(),
                'outputs': {}
            }
            
            task = Task(
                job_id=job_id,
                task_name=template_task.name,
                category=template_task.category,
                sequence_order=template_task.sequence_order,
                status=TaskStatus.PENDING,
                parameters=task_parameters,
                preferred_agent=template_task.preferred_agent
            )
            
            # Save task to database
            created_task = await db_manager.create_task(task)
            tasks.append(created_task)
        
        return tasks
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics and health information"""
        stats = await db_manager.get_system_stats()
        
        # Add template information
        if not template_loader.templates:
            await template_loader.load_all_templates()
        
        stats['templates_loaded'] = len(template_loader.templates)
        stats['database_connected'] = await db_manager.health_check()
        
        return stats
    
    async def test_llm_connection(self) -> Dict[str, Any]:
        """Test LLM service connection and return status"""
        try:
            async with LLMService() as llm_service:
                connected = await llm_service.test_connection()
                
                if connected:
                    usage_stats = await llm_service.get_usage_stats()
                    return {
                        "connected": True,
                        "status": "LLM service operational",
                        "usage_stats": usage_stats
                    }
                else:
                    return {
                        "connected": False,
                        "status": "LLM service connection failed",
                        "error": "Unable to connect to OpenRouter API"
                    }
        except ValueError as e:
            # API key not configured
            return {
                "connected": False,
                "status": "LLM service not configured",
                "error": str(e)
            }
        except Exception as e:
            return {
                "connected": False,
                "status": "LLM service error",
                "error": str(e)
            }
