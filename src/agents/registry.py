"""Agent registry for managing and discovering content generation agents"""

import logging
from typing import Dict, List, Optional, Type, Any
from ..core.models import Task, TaskCategory
from .base_agent import BaseAgent
from .llm_agent import LLMAgent

# Import specific agents
from .script.research_agent import ResearchAgent
from .script.writing_agent import WritingAgent
from .script.placeholder_agent import PlaceholderScriptAgent
from .image.design_agent import DesignAgent
from .image.freepik_agent import FreepikMysticAgent
from .audio.audio_agent import AudioAgent
from .video.video_agent import VideoAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry for managing and discovering content generation agents"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._category_agents: Dict[TaskCategory, List[BaseAgent]] = {
            TaskCategory.SCRIPT: [],
            TaskCategory.IMAGE: [],
            TaskCategory.AUDIO: [],
            TaskCategory.VIDEO: []
        }
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize default high-quality agents"""
        logger.info("Initializing agent registry with default agents...")
        
        # Register script agents
        self.register_agent_class("research_agent", ResearchAgent)
        self.register_agent_class("writing_agent", WritingAgent)
        self.register_agent_class("placeholder_script", PlaceholderScriptAgent)
        
        # Register image agents
        self.register_agent_class("design_agent", DesignAgent)
        self.register_agent_class("freepik_agent", FreepikMysticAgent)
        
        # Register audio agents
        self.register_agent_class("audio_agent", AudioAgent)
        
        # Register video agents
        self.register_agent_class("video_agent", VideoAgent)
        
        # Create default instances
        self.create_agent_instance("research_agent", "default_research")
        self.create_agent_instance("writing_agent", "default_writing")
        self.create_agent_instance("design_agent", "default_design")
        
        # Create Freepik agent with configuration
        freepik_config = self._get_freepik_config()
        self.create_agent_instance("freepik_agent", "freepik_mystic", freepik_config)
        self.create_agent_instance("audio_agent", "default_audio")
        self.create_agent_instance("video_agent", "default_video")
        self.create_agent_instance("placeholder_script", "fallback_script")
        
        logger.info(f"Agent registry initialized with {len(self._agents)} agents")
    
    def _get_freepik_config(self) -> Dict[str, Any]:
        """Get Freepik API configuration from centralized settings"""
        from ..core.config import settings
        
        config = {}
        
        # Get API key from centralized settings
        if settings.freepik_api_key:
            config['freepik_api_key'] = settings.freepik_api_key
            logger.info("Freepik API key loaded from configuration")
        else:
            logger.warning("Freepik API key not found. Agent will create specifications only.")
        
        # Optional webhook URL for async notifications
        if settings.freepik_webhook_url:
            config['webhook_url'] = settings.freepik_webhook_url
        
        return config
    
    def register_agent_class(self, agent_type: str, agent_class: Type[BaseAgent]):
        """Register an agent class for later instantiation"""
        self._agent_classes[agent_type] = agent_class
        logger.debug(f"Registered agent class: {agent_type}")
    
    def create_agent_instance(self, agent_type: str, instance_name: str, 
                            config: Optional[Dict[str, Any]] = None) -> BaseAgent:
        """Create and register an agent instance"""
        if agent_type not in self._agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = self._agent_classes[agent_type]
        agent = agent_class(config=config)
        
        self.register_agent_instance(instance_name, agent)
        return agent
    
    def register_agent_instance(self, instance_name: str, agent: BaseAgent):
        """Register an agent instance"""
        self._agents[instance_name] = agent
        self._category_agents[agent.category].append(agent)
        logger.debug(f"Registered agent instance: {instance_name} ({agent.category})")
    
    def get_agent(self, instance_name: str) -> Optional[BaseAgent]:
        """Get a specific agent instance by name"""
        return self._agents.get(instance_name)
    
    def get_agents_by_category(self, category: TaskCategory) -> List[BaseAgent]:
        """Get all agents for a specific category"""
        return self._category_agents.get(category, [])
    
    async def find_best_agent(self, task: Task) -> Optional[BaseAgent]:
        """Find the best agent for a specific task"""
        # First, check if task specifies a preferred agent
        if task.preferred_agent:
            preferred_agent = self.get_agent(task.preferred_agent)
            if preferred_agent:
                # Validate that preferred agent can handle the task
                try:
                    can_handle = await preferred_agent.validate_task(task)
                    if can_handle:
                        logger.info(f"Using template-specified agent {preferred_agent.name} for task {task.task_name}")
                        return preferred_agent
                    else:
                        logger.warning(f"Template-specified agent {preferred_agent.name} cannot handle task {task.task_name}, falling back to automatic selection")
                except Exception as e:
                    logger.error(f"Error validating preferred agent {preferred_agent.name}: {e}")
            else:
                logger.warning(f"Template-specified agent '{task.preferred_agent}' not found, falling back to automatic selection")
        
        # Fallback to automatic agent selection
        category_agents = self.get_agents_by_category(task.category)
        
        if not category_agents:
            logger.warning(f"No agents available for category: {task.category}")
            return None
        
        # Score agents based on task compatibility
        agent_scores = []
        
        for agent in category_agents:
            try:
                # Check if agent can handle the task
                can_handle = await agent.validate_task(task)
                
                if can_handle:
                    # Calculate compatibility score
                    score = await self._calculate_agent_score(agent, task)
                    agent_scores.append((agent, score))
                    
            except Exception as e:
                logger.error(f"Error validating agent {agent.name} for task {task.id}: {e}")
                continue
        
        if not agent_scores:
            logger.warning(f"No compatible agents found for task: {task.task_name}")
            # Return fallback agent if available
            return self._get_fallback_agent(task.category)
        
        # Sort by score (highest first) and return best agent
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        best_agent = agent_scores[0][0]
        
        logger.info(f"Selected agent {best_agent.name} for task {task.task_name} (score: {agent_scores[0][1]:.2f})")
        return best_agent
    
    async def _calculate_agent_score(self, agent: BaseAgent, task: Task) -> float:
        """Calculate compatibility score between agent and task"""
        score = 0.0
        
        # Base score for category match
        if agent.category == task.category:
            score += 0.5
        
        # Bonus for LLM-powered agents (higher quality)
        if isinstance(agent, LLMAgent):
            score += 0.3
        
        # Extra bonus for API-integrated agents (actual generation)
        if hasattr(agent, 'api_key') and agent.api_key:
            score += 0.2
            logger.debug(f"API integration bonus for {agent.name}")
        
        # Prioritize Freepik agent for image tasks when API key is available
        if (task.category == TaskCategory.IMAGE and 
            isinstance(agent, FreepikMysticAgent) and 
            hasattr(agent, 'api_key') and agent.api_key):
            score += 0.3
            logger.debug(f"Freepik API priority bonus for {agent.name}")
        
        # Task name keyword matching
        task_name_lower = task.task_name.lower()
        agent_specializations = await agent._get_specializations()
        
        for specialization in agent_specializations:
            spec_words = specialization.lower().split()
            matching_words = sum(1 for word in spec_words if word in task_name_lower)
            if matching_words > 0:
                score += (matching_words / len(spec_words)) * 0.2
        
        return min(score, 1.0)
    
    def _get_fallback_agent(self, category: TaskCategory) -> Optional[BaseAgent]:
        """Get fallback agent for category"""
        fallback_names = {
            TaskCategory.SCRIPT: "fallback_script",
            TaskCategory.IMAGE: "fallback_image", 
            TaskCategory.AUDIO: "fallback_audio",
            TaskCategory.VIDEO: "fallback_video"
        }
        
        fallback_name = fallback_names.get(category)
        if fallback_name:
            return self.get_agent(fallback_name)
        
        # Return any agent from the category as last resort
        category_agents = self.get_agents_by_category(category)
        return category_agents[0] if category_agents else None
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all registered agents with their capabilities"""
        agent_list = {}
        
        for name, agent in self._agents.items():
            agent_list[name] = {
                'name': agent.name,
                'category': agent.category,
                'type': 'llm_powered' if isinstance(agent, LLMAgent) else 'placeholder',
                'instance_key': agent.instance_key
            }
        
        return agent_list
    
    async def get_agent_capabilities(self, instance_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed capabilities for a specific agent"""
        agent = self.get_agent(instance_name)
        if agent:
            return await agent.get_capabilities()
        return None
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        stats = {
            'total_agents': len(self._agents),
            'agents_by_category': {
                category.value: len(agents) 
                for category, agents in self._category_agents.items()
            },
            'agent_types': {},
            'registered_classes': list(self._agent_classes.keys())
        }
        
        # Count agent types
        for agent in self._agents.values():
            agent_type = 'llm_powered' if isinstance(agent, LLMAgent) else 'placeholder'
            stats['agent_types'][agent_type] = stats['agent_types'].get(agent_type, 0) + 1
        
        return stats


# Global agent registry instance
agent_registry = AgentRegistry()
