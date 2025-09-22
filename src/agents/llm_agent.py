"""LLM-powered agent base class for high-quality content generation"""

import json
import logging
import time
from abc import abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID

from ..core.models import Task, TaskResult, TaskStatus, TaskCategory
from ..llm.llm_service import LLMService
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class LLMAgent(BaseAgent):
    """Base class for LLM-powered agents with structured prompts and quality control"""
    
    def __init__(self, name: str, category: TaskCategory, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, category, config)
        self.model = config.get('model', 'openai/gpt-4o-mini') if config else 'openai/gpt-4o-mini'
        self.temperature = config.get('temperature', 0.7) if config else 0.7
        self.max_tokens = config.get('max_tokens', 2000) if config else 2000
        
    async def execute(self, task: Task) -> TaskResult:
        """Execute task using LLM with structured prompts and quality control"""
        logger.info(f"LLM agent {self.name} executing task: {task.task_name}")
        start_time = time.time()
        
        try:
            # Validate task compatibility
            if not await self.validate_task(task):
                return self._create_error_result(
                    task, 
                    f"Task {task.task_name} is not compatible with agent {self.name}",
                    time.time() - start_time
                )
            
            # Extract task context
            inputs = self._extract_task_inputs(task)
            requirements = self._extract_task_requirements(task)
            
            # Generate structured prompt
            system_prompt = await self._build_system_prompt(task, inputs, requirements)
            user_prompt = await self._build_user_prompt(task, inputs, requirements)
            
            # Execute LLM request
            async with LLMService() as llm_service:
                if not await llm_service.test_connection():
                    logger.warning(f"LLM service unavailable for {self.name}, using fallback")
                    return await self._fallback_execution(task, inputs, requirements, start_time)
                
                # Make LLM request
                from ..llm.models import LLMRequest
                request = LLMRequest(
                    model=self.model,
                    messages=[{"role": "user", "content": user_prompt}],
                    system_prompt=system_prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    metadata={
                        "agent_name": self.name,
                        "task_name": task.task_name,
                        "task_id": str(task.id)
                    }
                )
                
                response = await llm_service.client.chat_completion(request)
                
                # Parse and validate response
                outputs = await self._parse_llm_response(response.content, task, inputs, requirements)
                
                # Quality validation
                quality_score = await self._validate_quality(outputs, task, inputs, requirements)
                
                # Add metadata
                metadata = {
                    'agent_name': self.name,
                    'agent_type': 'llm_powered',
                    'model_used': response.model,
                    'tokens_used': response.usage.total_tokens,
                    'cost': response.usage.estimated_cost,
                    'quality_score': quality_score,
                    'temperature': self.temperature,
                    'execution_time': time.time() - start_time
                }
                
                return self._create_success_result(
                    task=task,
                    outputs=outputs,
                    metadata=metadata,
                    execution_time=time.time() - start_time
                )
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response for task {task.id}: {e}")
            return await self._fallback_execution(task, inputs, requirements, start_time)
            
        except Exception as e:
            logger.error(f"LLM agent {self.name} failed to execute task {task.id}: {e}")
            return self._create_error_result(task, str(e), time.time() - start_time)
    
    @abstractmethod
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build the system prompt for this agent type"""
        pass
    
    @abstractmethod
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build the user prompt for this specific task"""
        pass
    
    @abstractmethod
    async def _parse_llm_response(self, response: str, task: Task, inputs: Dict[str, Any], 
                                requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the LLM response"""
        pass
    
    async def _validate_quality(self, outputs: Dict[str, Any], task: Task, 
                              inputs: Dict[str, Any], requirements: Dict[str, Any]) -> float:
        """Validate output quality and return score (0.0 to 1.0)"""
        score = 0.0
        checks = 0
        
        # Basic completeness check
        if outputs and len(outputs) > 0:
            score += 0.3
        checks += 1
        
        # Content length check (if applicable)
        if 'content' in outputs:
            content = outputs['content']
            if isinstance(content, str) and len(content) > 50:
                score += 0.2
            checks += 1
        
        # Requirements fulfillment check
        required_fields = await self._get_required_output_fields()
        fulfilled = sum(1 for field in required_fields if field in outputs)
        if required_fields:
            score += (fulfilled / len(required_fields)) * 0.3
            checks += 1
        
        # Format validation
        if await self._validate_output_format(outputs):
            score += 0.2
        checks += 1
        
        return min(score, 1.0) if checks > 0 else 0.0
    
    async def _get_required_output_fields(self) -> List[str]:
        """Return list of required output fields for quality validation"""
        return ['content']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate that outputs are in the correct format"""
        return isinstance(outputs, dict) and len(outputs) > 0
    
    async def _fallback_execution(self, task: Task, inputs: Dict[str, Any], 
                                requirements: Dict[str, Any], start_time: float) -> TaskResult:
        """Fallback execution when LLM is unavailable"""
        logger.warning(f"Using fallback execution for {self.name}")
        
        # Create basic fallback output
        outputs = await self._create_fallback_output(task, inputs, requirements)
        
        return self._create_success_result(
            task=task,
            outputs=outputs,
            metadata={
                'agent_name': self.name,
                'agent_type': 'llm_fallback',
                'fallback_reason': 'LLM service unavailable',
                'quality_score': 0.5,
                'execution_time': time.time() - start_time
            },
            execution_time=time.time() - start_time
        )
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback output when LLM is unavailable"""
        return {
            'content': f"Fallback content generated for {task.task_name}. LLM service was unavailable.",
            'status': 'fallback_generated',
            'user_request': inputs.get('user_request', 'No request provided')
        }


class StructuredLLMAgent(LLMAgent):
    """LLM agent that enforces structured JSON output"""
    
    async def _parse_llm_response(self, response: str, task: Task, inputs: Dict[str, Any], 
                                requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON response with error handling"""
        try:
            # Try to extract JSON from response
            response = response.strip()
            
            # Handle cases where LLM wraps JSON in markdown
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            response = response.strip()
            
            # Parse JSON
            parsed = json.loads(response)
            
            # Validate structure
            if not isinstance(parsed, dict):
                raise ValueError("Response must be a JSON object")
            
            return parsed
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse structured response: {e}")
            logger.error(f"Raw response: {response[:200]}...")
            
            # Try to extract content manually as fallback
            return await self._extract_content_fallback(response, task, inputs, requirements)
    
    async def _extract_content_fallback(self, response: str, task: Task, inputs: Dict[str, Any], 
                                      requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content from malformed response as fallback"""
        return {
            'content': response,
            'status': 'parsed_with_fallback',
            'parsing_error': 'Failed to parse as structured JSON'
        }
    
    def _build_json_schema_prompt(self, schema: Dict[str, Any]) -> str:
        """Build a prompt section describing the expected JSON schema"""
        return f"""
IMPORTANT: Respond with valid JSON only. No markdown formatting, no explanations, just the JSON object.

Expected JSON structure:
{json.dumps(schema, indent=2)}

Your response must be valid JSON that matches this exact structure.
"""
