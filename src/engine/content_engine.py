"""Main Content Engine orchestration class"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from ..core.database import db_manager
from ..core.models import (
    Job, Task, JobStatus, TaskStatus, TaskCategory, 
    JobCreateRequest, JobResponse, TemplateTask
)
from ..templates.loader import template_loader
from .task_runner import TaskRunner

logger = logging.getLogger(__name__)


class ContentEngine:
    """Main orchestration class for content creation jobs"""
    
    def __init__(self):
        self.task_runner = TaskRunner()
    
    async def create_job(self, request: JobCreateRequest) -> JobResponse:
        """Create a new content generation job"""
        logger.info(f"Creating job for request: {request.user_request[:100]}...")
        
        try:
            # Load templates if not already loaded
            if not template_loader.templates:
                await template_loader.load_all_templates()
            
            # For Phase 1, use simple template selection
            # In Phase 2, this will be LLM-powered
            template = await self._select_template(request)
            
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
            
        except Exception as e:
            logger.error(f"Failed to create job: {e}")
            raise
    
    async def get_job_status(self, job_id: UUID) -> Optional[JobResponse]:
        """Get job status with tasks"""
        job = await db_manager.get_job(job_id)
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
    
    async def _select_template(self, request: JobCreateRequest) -> Optional[object]:
        """Select appropriate template for the request"""
        # Phase 1: Simple template selection
        # Phase 2: LLM-powered intelligent selection
        
        if request.template_name:
            # Use specified template
            template = template_loader.get_template(request.template_name)
            if template:
                logger.info(f"Using specified template: {request.template_name}")
                return template
            else:
                logger.warning(f"Specified template not found: {request.template_name}")
        
        # Simple keyword-based selection for Phase 1
        request_lower = request.user_request.lower()
        
        if any(word in request_lower for word in ['blog', 'article', 'post', 'write']):
            template = template_loader.get_template('blog-post')
            if template:
                logger.info("Auto-selected blog-post template based on keywords")
                return template
        
        if any(word in request_lower for word in ['video', 'tutorial', 'youtube', 'teach']):
            template = template_loader.get_template('youtube-tutorial')
            if template:
                logger.info("Auto-selected youtube-tutorial template based on keywords")
                return template
        
        # Default to first available template
        templates = template_loader.list_templates()
        if templates:
            default_template = template_loader.get_template(templates[0])
            logger.info(f"Using default template: {templates[0]}")
            return default_template
        
        logger.warning("No templates available")
        return None
    
    async def _generate_job_names(self, request: JobCreateRequest, template: Optional[object]) -> Dict[str, str]:
        """Generate technical and display names for the job"""
        # Phase 1: Simple name generation
        # Phase 2: LLM-powered intelligent naming
        
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
                parameters=task_parameters
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
