"""Pydantic models for LLM integration"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class LLMUsage(BaseModel):
    """Token usage tracking for LLM requests"""
    prompt_tokens: int = Field(..., description="Tokens used in prompt")
    completion_tokens: int = Field(..., description="Tokens used in completion")
    total_tokens: int = Field(..., description="Total tokens used")
    estimated_cost: float = Field(default=0.0, description="Estimated cost in USD")


class LLMRequest(BaseModel):
    """LLM request model"""
    id: UUID = Field(default_factory=uuid4)
    model: str = Field(..., description="Model identifier (e.g., openai/gpt-3.5-turbo)")
    messages: List[Dict[str, str]] = Field(..., description="Chat messages")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    system_prompt: Optional[str] = Field(default=None, description="System message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LLMResponse(BaseModel):
    """LLM response model"""
    id: UUID = Field(..., description="Request ID")
    model: str = Field(..., description="Model used")
    content: str = Field(..., description="Generated content")
    usage: LLMUsage = Field(..., description="Token usage information")
    finish_reason: str = Field(..., description="Completion finish reason")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    response_time: float = Field(..., description="Response time in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TemplateAnalysis(BaseModel):
    """LLM analysis of user request for template selection"""
    content_type: str = Field(..., description="Type of content (blog, tutorial, guide, etc.)")
    audience: str = Field(..., description="Target audience (beginners, professionals, general)")
    tone: str = Field(..., description="Content tone (formal, casual, technical, etc.)")
    complexity: str = Field(..., description="Content complexity (simple, intermediate, advanced)")
    estimated_length: str = Field(..., description="Estimated content length (short, medium, long)")
    recommended_template: str = Field(..., description="Best matching template")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    reasoning: str = Field(..., description="Explanation for template selection")


class JobNaming(BaseModel):
    """LLM-generated job naming suggestions"""
    primary_name: str = Field(..., description="Primary job name suggestion")
    display_name: str = Field(..., description="Human-readable display name")
    slug: str = Field(..., description="URL-friendly slug")
    alternatives: List[str] = Field(default_factory=list, description="Alternative name suggestions")
    seo_keywords: List[str] = Field(default_factory=list, description="SEO-relevant keywords")
    reasoning: str = Field(..., description="Explanation for naming choices")


class AgentSelection(BaseModel):
    """LLM-powered agent selection for tasks"""
    task_id: UUID = Field(..., description="Task ID")
    task_category: str = Field(..., description="Task category")
    recommended_agent: str = Field(..., description="Recommended agent identifier")
    agent_config: Dict[str, Any] = Field(default_factory=dict, description="Agent configuration")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Selection confidence")
    reasoning: str = Field(..., description="Selection reasoning")
    fallback_agents: List[str] = Field(default_factory=list, description="Fallback options")
