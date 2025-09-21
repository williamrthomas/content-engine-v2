"""Placeholder script generation agent for Phase 1"""

from ..base_agent import PlaceholderAgent
from ...core.models import TaskCategory


class PlaceholderScriptAgent(PlaceholderAgent):
    """Placeholder agent for script generation tasks"""
    
    def __init__(self, config=None):
        super().__init__(
            name="Placeholder Script Agent",
            category=TaskCategory.SCRIPT,
            config=config
        )
    
    async def _get_specializations(self) -> list:
        """Script-specific specializations"""
        return [
            "Blog post writing",
            "Article creation", 
            "Content research",
            "SEO optimization",
            "Headline generation",
            "Meta description writing"
        ]
