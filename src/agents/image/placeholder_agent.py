"""Placeholder image generation agent for Phase 1"""

from ..base_agent import PlaceholderAgent
from ...core.models import TaskCategory


class PlaceholderImageAgent(PlaceholderAgent):
    """Placeholder agent for image generation tasks"""
    
    def __init__(self, config=None):
        super().__init__(
            name="Placeholder Image Agent",
            category=TaskCategory.IMAGE,
            config=config
        )
    
    async def _get_specializations(self) -> list:
        """Image-specific specializations"""
        return [
            "Featured image creation",
            "Social media graphics",
            "Blog post illustrations",
            "Thumbnail design",
            "Infographic creation",
            "Brand-consistent visuals"
        ]
