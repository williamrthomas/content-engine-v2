"""Placeholder video generation agent for Phase 1"""

from ..base_agent import PlaceholderAgent
from ...core.models import TaskCategory


class PlaceholderVideoAgent(PlaceholderAgent):
    """Placeholder agent for video generation tasks"""
    
    def __init__(self, config=None):
        super().__init__(
            name="Placeholder Video Agent",
            category=TaskCategory.VIDEO,
            config=config
        )
    
    async def _get_specializations(self) -> list:
        """Video-specific specializations"""
        return [
            "Tutorial video creation",
            "Slideshow presentations",
            "Social media videos",
            "Product demonstrations",
            "Educational content",
            "Promotional videos"
        ]
