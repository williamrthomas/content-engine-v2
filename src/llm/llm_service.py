"""Main LLM service for intelligent content decisions"""

import json
import logging
from typing import Dict, List, Optional, Any
from uuid import UUID

from ..core.config import settings
from ..templates.loader import template_loader
from .openrouter_client import OpenRouterClient
from .models import (
    LLMRequest, LLMResponse, TemplateAnalysis, 
    JobNaming, AgentSelection
)

logger = logging.getLogger(__name__)


class LLMService:
    """Main service for LLM-powered intelligent decisions"""
    
    def __init__(self):
        self.client = OpenRouterClient()
        self.default_model = settings.default_model
        self.fallback_model = settings.fallback_model
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def test_connection(self) -> bool:
        """Test LLM service connection"""
        return await self.client.test_connection()
    
    async def analyze_for_template_selection(self, user_request: str) -> TemplateAnalysis:
        """Analyze user request to select the best template"""
        
        # Get available templates
        await template_loader.load_all_templates()
        templates = template_loader.list_templates()
        
        # Build template descriptions
        template_descriptions = {}
        for template_name in templates:
            template = template_loader.get_template(template_name)
            if template:
                # Count tasks by category
                categories = {}
                for task in template.tasks:
                    categories[task.category] = categories.get(task.category, 0) + 1
                
                template_descriptions[template_name] = {
                    "title": template.title,
                    "description": template.description,
                    "category": template.category,
                    "tasks": len(template.tasks),
                    "task_breakdown": categories
                }
        
        system_prompt = """You are an expert content strategist who analyzes user requests to recommend the best content template.

Your job is to analyze the user's request and recommend the most suitable template based on:
- Content type and format
- Target audience and complexity
- Tone and style requirements
- Estimated scope and length

Respond with a JSON object containing your analysis."""
        
        user_prompt = f"""
User Request: "{user_request}"

Available Templates:
{json.dumps(template_descriptions, indent=2)}

Analyze this request and provide your recommendation as a JSON object with these fields:
- content_type: Type of content (blog, tutorial, guide, etc.)
- audience: Target audience (beginners, professionals, general)
- tone: Content tone (formal, casual, technical, etc.)
- complexity: Content complexity (simple, intermediate, advanced)
- estimated_length: Estimated content length (short, medium, long)
- recommended_template: Best matching template name
- confidence: Confidence score (0.0 to 1.0)
- reasoning: Detailed explanation for your choice

Be specific and consider the user's exact wording and implied needs.
"""
        
        request = LLMRequest(
            model=self.default_model,
            messages=[{"role": "user", "content": user_prompt}],
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=500,
            metadata={"purpose": "template_selection", "user_request": user_request}
        )
        
        try:
            response = await self.client.chat_completion(request)
            
            # Parse JSON response
            analysis_data = json.loads(response.content)
            
            # Validate recommended template exists
            if analysis_data["recommended_template"] not in templates:
                logger.warning(f"LLM recommended non-existent template: {analysis_data['recommended_template']}")
                # Fallback to first available template
                analysis_data["recommended_template"] = templates[0] if templates else "blog-post"
                analysis_data["confidence"] = 0.5
                analysis_data["reasoning"] += " (Fallback due to invalid recommendation)"
            
            return TemplateAnalysis(**analysis_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response content: {response.content}")
            # Fallback to simple keyword-based selection
            return self._fallback_template_selection(user_request, templates)
        
        except Exception as e:
            logger.error(f"Error in template analysis: {e}")
            return self._fallback_template_selection(user_request, templates)
    
    def _fallback_template_selection(self, user_request: str, templates: List[str]) -> TemplateAnalysis:
        """Fallback template selection using keyword matching"""
        request_lower = user_request.lower()
        
        # Simple keyword matching
        if any(word in request_lower for word in ["tutorial", "guide", "how to", "learn", "teach"]):
            recommended = "youtube-tutorial" if "youtube-tutorial" in templates else templates[0]
            content_type = "tutorial"
        else:
            recommended = "blog-post" if "blog-post" in templates else templates[0]
            content_type = "blog"
        
        return TemplateAnalysis(
            content_type=content_type,
            audience="general",
            tone="informative",
            complexity="intermediate",
            estimated_length="medium",
            recommended_template=recommended,
            confidence=0.6,
            reasoning="Fallback keyword-based selection due to LLM analysis failure"
        )
    
    async def generate_job_name(self, user_request: str, template_name: str) -> JobNaming:
        """Generate intelligent job names based on user request"""
        
        system_prompt = """You are an expert at creating clear, SEO-friendly, and descriptive job names for content creation projects.

Create job names that are:
- Clear and descriptive
- SEO-optimized with relevant keywords
- Professional but engaging
- Suitable for both internal tracking and public display

Respond with a JSON object containing your suggestions."""
        
        user_prompt = f"""
User Request: "{user_request}"
Template: {template_name}

Generate job naming suggestions as a JSON object with these fields:
- primary_name: Main job name (concise, descriptive)
- display_name: Human-readable display name (can be longer)
- slug: URL-friendly slug (lowercase, hyphens)
- alternatives: List of 2-3 alternative names
- seo_keywords: List of relevant SEO keywords
- reasoning: Brief explanation of naming strategy

Make the names specific to the content request while being professional and searchable.
"""
        
        request = LLMRequest(
            model=self.default_model,
            messages=[{"role": "user", "content": user_prompt}],
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=400,
            metadata={"purpose": "job_naming", "user_request": user_request}
        )
        
        try:
            response = await self.client.chat_completion(request)
            naming_data = json.loads(response.content)
            return JobNaming(**naming_data)
            
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error in job naming: {e}")
            # Fallback to simple naming
            return self._fallback_job_naming(user_request)
    
    def _fallback_job_naming(self, user_request: str) -> JobNaming:
        """Fallback job naming strategy"""
        # Simple truncation and cleaning
        clean_request = user_request.strip()[:50]
        slug = clean_request.lower().replace(" ", "-").replace("'", "")
        
        return JobNaming(
            primary_name=f"Content: {clean_request}",
            display_name=clean_request,
            slug=slug,
            alternatives=[f"Project: {clean_request}", f"Task: {clean_request}"],
            seo_keywords=clean_request.split()[:5],
            reasoning="Fallback naming due to LLM generation failure"
        )
    
    async def select_agent_for_task(self, task_id: UUID, task_category: str, 
                                  task_name: str, context: Dict[str, Any]) -> AgentSelection:
        """Select the best agent for a specific task"""
        
        # For now, return placeholder selection since we don't have real agents yet
        # This will be enhanced when we implement real agents in Phase 3
        
        return AgentSelection(
            task_id=task_id,
            task_category=task_category,
            recommended_agent=f"placeholder_{task_category}_agent",
            agent_config={"mode": "standard", "quality": "high"},
            confidence=0.8,
            reasoning=f"Placeholder agent selection for {task_category} tasks",
            fallback_agents=[f"fallback_{task_category}_agent"]
        )
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get LLM usage statistics"""
        # This would track usage across all requests
        # For now, return placeholder stats
        return {
            "total_requests": 0,
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "models_used": [],
            "average_response_time": 0.0
        }
