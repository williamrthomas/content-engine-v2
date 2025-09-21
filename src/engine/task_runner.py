"""Sequential task execution engine"""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from ..core.database import db_manager
from ..core.models import Task, TaskStatus, TaskCategory, TaskResult
from ..agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TaskRunner:
    """Handles sequential execution of tasks within jobs"""
    
    def __init__(self):
        self.agents_registry: Dict[str, BaseAgent] = {}
    
    async def process_job(self, job_id: UUID) -> bool:
        """Process all tasks for a job in sequential order by category"""
        logger.info(f"Processing job {job_id}")
        
        try:
            # Define execution order (strict sequence)
            categories = [TaskCategory.SCRIPT, TaskCategory.IMAGE, TaskCategory.AUDIO, TaskCategory.VIDEO]
            
            for category in categories:
                success = await self._process_category(job_id, category)
                if not success:
                    logger.error(f"Failed to process {category} tasks for job {job_id}")
                    return False
                
                logger.info(f"Completed {category} tasks for job {job_id}")
            
            logger.info(f"Successfully completed all tasks for job {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Job processing failed for {job_id}: {e}")
            return False
    
    async def _process_category(self, job_id: UUID, category: TaskCategory) -> bool:
        """Process all tasks in a specific category"""
        logger.info(f"Processing {category} tasks for job {job_id}")
        
        try:
            # Get all tasks for this category
            tasks = await db_manager.get_tasks_for_category(job_id, category)
            
            if not tasks:
                logger.info(f"No {category} tasks found for job {job_id}")
                return True
            
            # Process tasks in sequence order
            for task in sorted(tasks, key=lambda t: t.sequence_order):
                success = await self._process_task(task)
                if not success:
                    logger.error(f"Failed to process task {task.id} ({task.task_name})")
                    return False
                
                logger.info(f"Completed task {task.id} ({task.task_name})")
            
            return True
            
        except Exception as e:
            logger.error(f"Category processing failed for {category} in job {job_id}: {e}")
            return False
    
    async def _process_task(self, task: Task) -> bool:
        """Process a single task"""
        logger.info(f"Processing task {task.id}: {task.task_name}")
        
        try:
            # Update task status to in_progress
            await db_manager.update_task_status(
                task.id, 
                TaskStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            )
            
            # For Phase 1, we'll use placeholder execution
            # Phase 2 will add LLM agent selection
            # Phase 3 will add real agent implementations
            result = await self._execute_task_placeholder(task)
            
            if result.status == TaskStatus.COMPLETED:
                # Update task with success
                await db_manager.update_task_status(
                    task.id,
                    TaskStatus.COMPLETED,
                    completed_at=datetime.utcnow()
                )
                
                # Update task parameters with outputs
                updated_params = task.parameters.copy()
                updated_params['outputs'] = result.outputs
                await db_manager.update_task_parameters(task.id, updated_params)
                
                logger.info(f"Task {task.id} completed successfully")
                return True
            else:
                # Update task with failure
                await db_manager.update_task_status(
                    task.id,
                    TaskStatus.FAILED,
                    completed_at=datetime.utcnow(),
                    error_message=result.error_message
                )
                
                logger.error(f"Task {task.id} failed: {result.error_message}")
                return False
                
        except Exception as e:
            # Update task with error
            await db_manager.update_task_status(
                task.id,
                TaskStatus.FAILED,
                completed_at=datetime.utcnow(),
                error_message=str(e)
            )
            
            logger.error(f"Task execution failed for {task.id}: {e}")
            return False
    
    async def _execute_task_placeholder(self, task: Task) -> TaskResult:
        """Placeholder task execution for Phase 1"""
        logger.info(f"Executing placeholder for task: {task.task_name}")
        
        # Simulate some processing time
        await asyncio.sleep(0.5)
        
        # Generate placeholder outputs based on task category and name
        outputs = self._generate_placeholder_outputs(task)
        
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.COMPLETED,
            outputs=outputs,
            files={},
            metadata={
                'execution_type': 'placeholder',
                'processed_at': datetime.utcnow().isoformat()
            },
            execution_time=0.5
        )
    
    def _generate_placeholder_outputs(self, task: Task) -> Dict[str, Any]:
        """Generate realistic placeholder outputs for different task types"""
        base_outputs = {
            'task_name': task.task_name,
            'category': task.category,
            'status': 'completed',
            'processed_at': datetime.utcnow().isoformat()
        }
        
        # Category-specific placeholder outputs
        if task.category == TaskCategory.SCRIPT:
            if 'research' in task.task_name.lower():
                base_outputs.update({
                    'research_notes': f"Research findings for {task.task_name}",
                    'sources_found': 5,
                    'key_points': ["Point 1", "Point 2", "Point 3"]
                })
            elif 'headline' in task.task_name.lower() or 'title' in task.task_name.lower():
                base_outputs.update({
                    'headlines': [
                        "Compelling Headline Option 1",
                        "Engaging Title Option 2", 
                        "SEO-Optimized Headline 3"
                    ],
                    'meta_description': "SEO-optimized meta description for the content"
                })
            elif 'write' in task.task_name.lower():
                base_outputs.update({
                    'content': f"Generated content for {task.task_name}",
                    'word_count': 500,
                    'readability_score': 8.5
                })
            else:
                base_outputs.update({
                    'content': f"Generated script content for {task.task_name}",
                    'word_count': 300
                })
        
        elif task.category == TaskCategory.IMAGE:
            base_outputs.update({
                'image_description': f"Generated image for {task.task_name}",
                'dimensions': "1200x630",
                'format': "png",
                'style': "professional"
            })
        
        elif task.category == TaskCategory.AUDIO:
            base_outputs.update({
                'audio_description': f"Generated audio for {task.task_name}",
                'duration': "2:30",
                'format': "mp3",
                'voice_style': "professional"
            })
        
        elif task.category == TaskCategory.VIDEO:
            base_outputs.update({
                'video_description': f"Generated video for {task.task_name}",
                'duration': "5:00",
                'format': "mp4",
                'resolution': "1080p"
            })
        
        return base_outputs
    
    async def get_next_pending_task(self, job_id: UUID) -> Optional[Task]:
        """Get the next pending task for a job"""
        return await db_manager.get_next_pending_task(job_id)
    
    async def register_agent(self, agent_key: str, agent: BaseAgent) -> None:
        """Register an agent for task execution"""
        self.agents_registry[agent_key] = agent
        logger.info(f"Registered agent: {agent_key}")
    
    async def get_available_agents(self, category: TaskCategory) -> List[str]:
        """Get available agents for a specific category"""
        # For Phase 1, return empty list (using placeholders)
        # Phase 3 will implement real agent discovery
        return []
