"""Pydantic data models for Content Engine V2"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskCategory(str, Enum):
    """Task category enumeration"""
    SCRIPT = "script"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    DISABLED = "disabled"


# Database Models

class Job(BaseModel):
    """Job model matching the database schema"""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., max_length=200, description="Technical job name")
    display_name: Optional[str] = Field(None, max_length=200, description="Human-readable job name")
    template_name: Optional[str] = Field(None, max_length=100, description="Template used for this job")
    user_request: Optional[str] = Field(None, description="Original user request")
    status: JobStatus = Field(default=JobStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


class Task(BaseModel):
    """Task model matching the database schema"""
    id: UUID = Field(default_factory=uuid4)
    job_id: UUID = Field(..., description="Reference to parent job")
    task_name: str = Field(..., max_length=100, description="Free-form task description")
    category: TaskCategory = Field(..., description="Task category")
    sequence_order: int = Field(..., description="Order within category")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    assigned_agent_id: Optional[UUID] = Field(None, description="Assigned agent ID")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters as JSONB")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        use_enum_values = True


class Agent(BaseModel):
    """Agent model matching the database schema"""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., max_length=100, description="Human-readable agent name")
    instance_key: str = Field(..., max_length=50, description="Unique instance identifier")
    category: TaskCategory = Field(..., description="Agent category")
    provider: Optional[str] = Field(None, max_length=50, description="Service provider")
    model: Optional[str] = Field(None, max_length=50, description="Model identifier")
    specialization: Optional[str] = Field(None, description="Agent specialization description")
    config: Dict[str, Any] = Field(default_factory=dict, description="Agent configuration")
    status: AgentStatus = Field(default=AgentStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


# API Models

class JobCreateRequest(BaseModel):
    """Request model for creating a new job"""
    user_request: str = Field(..., description="User's content creation request")
    template_name: Optional[str] = Field(None, description="Specific template to use (optional)")


class JobResponse(BaseModel):
    """Response model for job operations"""
    job: Job
    tasks: List[Task] = Field(default_factory=list)


class TaskResult(BaseModel):
    """Result model for task execution"""
    task_id: UUID
    status: TaskStatus
    outputs: Dict[str, Any] = Field(default_factory=dict)
    files: Dict[str, str] = Field(default_factory=dict, description="Generated file paths")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class AgentSelection(BaseModel):
    """Model for LLM agent selection response"""
    agent_id: UUID
    agent_name: str
    reasoning: str = Field(..., description="Why this agent was selected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Selection confidence")


class TemplateSelection(BaseModel):
    """Model for LLM template selection response"""
    template_name: str
    reasoning: str = Field(..., description="Why this template was selected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Selection confidence")


class JobNaming(BaseModel):
    """Model for LLM job naming response"""
    technical_name: str = Field(..., description="Technical job name for filesystem")
    display_name: str = Field(..., description="Human-readable display name")
    reasoning: str = Field(..., description="Naming rationale")


# Template Models

class TemplateTask(BaseModel):
    """Model for tasks defined in templates"""
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    category: TaskCategory = Field(..., description="Task category")
    sequence_order: int = Field(..., description="Order within category")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Default parameters")


class Template(BaseModel):
    """Model for content templates"""
    name: str = Field(..., description="Template name")
    title: str = Field(..., description="Template title")
    description: str = Field(..., description="Template description")
    category: str = Field(..., description="Content category")
    tasks: List[TemplateTask] = Field(..., description="Template tasks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# System Models

class SystemStatus(BaseModel):
    """System status information"""
    database_connected: bool
    total_jobs: int
    active_jobs: int
    total_agents: int
    active_agents: int
    templates_loaded: int
