"""Base agent class for content generation"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from ..core.models import Task, TaskResult, TaskStatus, TaskCategory

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all content generation agents"""
    
    def __init__(self, name: str, category: TaskCategory, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.category = category
        self.config = config or {}
        self.instance_key = self._generate_instance_key()
    
    def _generate_instance_key(self) -> str:
        """Generate a unique instance key for this agent"""
        # Convert name to snake_case
        key = self.name.lower().replace(' ', '_').replace('-', '_')
        # Remove special characters
        key = ''.join(c for c in key if c.isalnum() or c == '_')
        return key
    
    @abstractmethod
    async def execute(self, task: Task) -> TaskResult:
        """Execute a task and return results"""
        pass
    
    @abstractmethod
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the given task"""
        pass
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities and specializations"""
        return {
            'name': self.name,
            'category': self.category,
            'instance_key': self.instance_key,
            'specializations': await self._get_specializations(),
            'supported_parameters': await self._get_supported_parameters(),
            'output_formats': await self._get_output_formats()
        }
    
    async def _get_specializations(self) -> list:
        """Return list of agent specializations"""
        return []
    
    async def _get_supported_parameters(self) -> list:
        """Return list of supported task parameters"""
        return []
    
    async def _get_output_formats(self) -> list:
        """Return list of supported output formats"""
        return []
    
    def _extract_task_inputs(self, task: Task) -> Dict[str, Any]:
        """Extract input parameters from task"""
        return task.parameters.get('inputs', {})
    
    def _extract_task_requirements(self, task: Task) -> Dict[str, Any]:
        """Extract requirement parameters from task"""
        return task.parameters.get('requirements', {})
    
    def _create_success_result(self, task: Task, outputs: Dict[str, Any], 
                             files: Optional[Dict[str, str]] = None,
                             metadata: Optional[Dict[str, Any]] = None,
                             execution_time: Optional[float] = None) -> TaskResult:
        """Create a successful task result"""
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.COMPLETED,
            outputs=outputs,
            files=files or {},
            metadata=metadata or {},
            execution_time=execution_time
        )
    
    def _create_error_result(self, task: Task, error_message: str,
                           execution_time: Optional[float] = None) -> TaskResult:
        """Create a failed task result"""
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.FAILED,
            outputs={},
            files={},
            metadata={},
            error_message=error_message,
            execution_time=execution_time
        )
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name} ({self.category})>"


class PlaceholderAgent(BaseAgent):
    """Placeholder agent for Phase 1 development"""
    
    def __init__(self, name: str, category: TaskCategory, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, category, config)
    
    async def execute(self, task: Task) -> TaskResult:
        """Execute task with placeholder logic"""
        logger.info(f"Placeholder agent {self.name} executing task: {task.task_name}")
        
        try:
            inputs = self._extract_task_inputs(task)
            requirements = self._extract_task_requirements(task)
            
            # Generate placeholder outputs based on task and category
            outputs = await self._generate_placeholder_outputs(task, inputs, requirements)
            
            return self._create_success_result(
                task=task,
                outputs=outputs,
                metadata={
                    'agent_name': self.name,
                    'agent_type': 'placeholder',
                    'processed_at': datetime.utcnow().isoformat()
                },
                execution_time=0.1
            )
            
        except Exception as e:
            logger.error(f"Placeholder agent {self.name} failed to execute task {task.id}: {e}")
            return self._create_error_result(task, str(e))
    
    async def validate_task(self, task: Task) -> bool:
        """Validate task - placeholder agents accept all tasks in their category"""
        return task.category == self.category
    
    async def _generate_placeholder_outputs(self, task: Task, inputs: Dict[str, Any], 
                                          requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic placeholder outputs"""
        base_outputs = {
            'task_name': task.task_name,
            'agent_used': self.name,
            'category': self.category,
            'user_request': inputs.get('user_request', 'No request provided')
        }
        
        # Category-specific outputs
        if self.category == TaskCategory.SCRIPT:
            return await self._generate_script_outputs(task, inputs, requirements, base_outputs)
        elif self.category == TaskCategory.IMAGE:
            return await self._generate_image_outputs(task, inputs, requirements, base_outputs)
        elif self.category == TaskCategory.AUDIO:
            return await self._generate_audio_outputs(task, inputs, requirements, base_outputs)
        elif self.category == TaskCategory.VIDEO:
            return await self._generate_video_outputs(task, inputs, requirements, base_outputs)
        
        return base_outputs
    
    async def _generate_script_outputs(self, task: Task, inputs: Dict[str, Any], 
                                     requirements: Dict[str, Any], base: Dict[str, Any]) -> Dict[str, Any]:
        """Generate script-specific placeholder outputs"""
        task_name_lower = task.task_name.lower()
        
        if 'research' in task_name_lower:
            base.update({
                'research_summary': f"Comprehensive research on {inputs.get('user_request', 'the topic')}",
                'key_findings': [
                    "Finding 1: Important insight about the topic",
                    "Finding 2: Statistical data supporting the content",
                    "Finding 3: Expert opinion or case study"
                ],
                'sources': [
                    "https://example.com/source1",
                    "https://example.com/source2", 
                    "https://example.com/source3"
                ],
                'source_count': requirements.get('min_sources', 3)
            })
        
        elif any(word in task_name_lower for word in ['headline', 'title']):
            base.update({
                'headlines': [
                    f"Compelling Title About {inputs.get('user_request', 'Your Topic')}",
                    f"How to Master {inputs.get('user_request', 'This Subject')} in 2024",
                    f"The Ultimate Guide to {inputs.get('user_request', 'Success')}"
                ],
                'meta_description': f"Learn everything about {inputs.get('user_request', 'this topic')} with our comprehensive guide.",
                'seo_optimized': requirements.get('seo_optimized', True)
            })
        
        elif 'write' in task_name_lower or 'content' in task_name_lower:
            target_words = requirements.get('target_words', requirements.get('word_count', 500))
            base.update({
                'content': f"# Generated Content for {task.task_name}\n\nThis is placeholder content generated for the task '{task.task_name}'. In a real implementation, this would contain the actual written content based on the user request: {inputs.get('user_request', 'No request provided')}.\n\nThe content would be approximately {target_words} words and would include all the requirements specified in the task parameters.",
                'word_count': target_words,
                'readability_score': 8.2,
                'tone': requirements.get('tone', 'professional'),
                'includes_cta': requirements.get('include_cta', False)
            })
        
        else:
            base.update({
                'content': f"Generated script content for {task.task_name}",
                'word_count': 300,
                'format': 'markdown'
            })
        
        return base
    
    async def _generate_image_outputs(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any], base: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image-specific placeholder outputs"""
        base.update({
            'image_description': f"Professional image generated for {task.task_name}",
            'dimensions': requirements.get('size', '1200x630'),
            'format': 'png',
            'style': requirements.get('style', 'professional'),
            'includes_text': requirements.get('include_text', False),
            'color_scheme': 'brand_colors' if requirements.get('brand_colors') else 'default'
        })
        return base
    
    async def _generate_audio_outputs(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any], base: Dict[str, Any]) -> Dict[str, Any]:
        """Generate audio-specific placeholder outputs"""
        base.update({
            'audio_description': f"Professional audio generated for {task.task_name}",
            'duration': requirements.get('duration', '2:30'),
            'format': requirements.get('format', 'mp3'),
            'voice_style': requirements.get('voice_style', 'professional'),
            'speed': requirements.get('speed', 'normal'),
            'includes_music': requirements.get('include_intro_music', False)
        })
        return base
    
    async def _generate_video_outputs(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any], base: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video-specific placeholder outputs"""
        base.update({
            'video_description': f"Professional video generated for {task.task_name}",
            'duration': requirements.get('duration', '5:00'),
            'format': requirements.get('format', 'mp4'),
            'resolution': requirements.get('resolution', '1080p'),
            'style': requirements.get('style', 'slideshow'),
            'includes_narration': requirements.get('include_narration', True),
            'includes_captions': requirements.get('include_captions', False)
        })
        return base
    
    async def _get_specializations(self) -> list:
        """Return placeholder agent specializations"""
        return [f"Placeholder {self.category} generation", "Development testing", "Phase 1 implementation"]
    
    async def _get_supported_parameters(self) -> list:
        """Return supported parameters for placeholder agents"""
        common_params = ['user_request', 'template_name', 'job_id']
        
        if self.category == TaskCategory.SCRIPT:
            return common_params + ['word_count', 'tone', 'seo_optimized', 'include_cta']
        elif self.category == TaskCategory.IMAGE:
            return common_params + ['size', 'style', 'include_text', 'brand_colors']
        elif self.category == TaskCategory.AUDIO:
            return common_params + ['duration', 'format', 'voice_style', 'speed']
        elif self.category == TaskCategory.VIDEO:
            return common_params + ['duration', 'format', 'resolution', 'style']
        
        return common_params
    
    async def _get_output_formats(self) -> list:
        """Return supported output formats"""
        if self.category == TaskCategory.SCRIPT:
            return ['markdown', 'text', 'html']
        elif self.category == TaskCategory.IMAGE:
            return ['png', 'jpg', 'svg']
        elif self.category == TaskCategory.AUDIO:
            return ['mp3', 'wav', 'aac']
        elif self.category == TaskCategory.VIDEO:
            return ['mp4', 'mov', 'webm']
        
        return ['json']
