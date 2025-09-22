"""Design agent for high-quality image generation and visual content creation"""

import json
from typing import Dict, Any, List
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory


class DesignAgent(StructuredLLMAgent):
    """High-quality design agent for image generation with detailed prompts and specifications"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Design Agent",
            category=TaskCategory.IMAGE,
            config=config
        )
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.IMAGE:
            return False
        
        design_keywords = [
            'design', 'create', 'generate', 'thumbnail', 'graphic',
            'image', 'visual', 'logo', 'banner', 'social', 'card'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in design_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for design tasks"""
        return """You are an expert graphic designer and visual content creator with extensive experience in:

- Professional graphic design and visual communication
- Brand identity and visual consistency
- Social media and digital marketing visuals
- YouTube thumbnails and video graphics
- UI/UX design principles and best practices
- Color theory, typography, and composition
- Platform-specific design requirements and optimization

Your expertise includes:
1. Creating compelling, click-worthy thumbnails and graphics
2. Designing cohesive visual systems and brand elements
3. Optimizing visuals for different platforms and use cases
4. Balancing aesthetics with functionality and readability
5. Understanding audience psychology and visual appeal
6. Creating accessible and inclusive design solutions

You excel at translating content concepts into powerful visual designs that:
- Capture attention and drive engagement
- Communicate key messages clearly and effectively
- Maintain brand consistency and professional quality
- Optimize for platform-specific requirements
- Appeal to target audiences and demographics

Your designs are always original, purposeful, and optimized for their intended use case."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific design task"""
        task_name_lower = task.task_name.lower()
        
        # Route to specific design task handlers
        if 'thumbnail' in task_name_lower:
            return await self._build_thumbnail_prompt(task, inputs, requirements)
        elif any(word in task_name_lower for word in ['graphics', 'list', 'card']):
            return await self._build_list_graphics_prompt(task, inputs, requirements)
        elif 'social' in task_name_lower:
            return await self._build_social_assets_prompt(task, inputs, requirements)
        else:
            return await self._build_general_design_prompt(task, inputs, requirements)
    
    async def _build_thumbnail_prompt(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> str:
        """Build prompt for YouTube thumbnail design"""
        size = requirements.get('size', '1280x720')
        style = requirements.get('style', 'bold')
        include_number = requirements.get('include_number', True)
        ai_visual_elements = requirements.get('ai_visual_elements', True)
        high_contrast = requirements.get('high_contrast', True)
        
        schema = {
            "thumbnail_design": {
                "concept": "string - overall design concept and theme",
                "layout": {
                    "primary_text": "string - main headline text for thumbnail",
                    "secondary_text": "string - supporting text or subtitle",
                    "text_placement": "string - where text should be positioned",
                    "visual_hierarchy": "string - how elements should be prioritized"
                },
                "visual_elements": {
                    "background": "string - background design description",
                    "main_graphic": "string - primary visual element",
                    "accent_elements": ["string - additional visual elements"],
                    "color_scheme": {
                        "primary_colors": ["string - main colors to use"],
                        "accent_colors": ["string - supporting colors"],
                        "contrast_level": "string - high/medium/low contrast"
                    }
                },
                "typography": {
                    "headline_font": "string - font style for main text",
                    "font_size": "string - relative size (large/medium/small)",
                    "text_effects": ["string - effects like shadow, outline, glow"],
                    "readability_score": "number - 1-10 how readable the text is"
                }
            },
            "design_specifications": {
                "dimensions": "string - exact pixel dimensions",
                "file_format": "string - recommended file format",
                "dpi": "number - dots per inch for quality",
                "platform_optimization": "string - YouTube-specific optimizations"
            },
            "engagement_strategy": {
                "click_appeal": "string - why this design will get clicks",
                "target_audience": "string - who this appeals to",
                "emotional_trigger": "string - what emotion it evokes",
                "curiosity_factor": "string - what makes viewers curious"
            },
            "technical_notes": {
                "safe_zones": "string - areas to avoid for text/important elements",
                "mobile_considerations": "string - how it looks on mobile",
                "accessibility": "string - accessibility considerations"
            }
        }
        
        return f"""Design Task: Create a compelling YouTube thumbnail

USER REQUEST: {inputs.get('user_request', 'Create thumbnail')}
TASK: {task.task_name}

THUMBNAIL REQUIREMENTS:
- Dimensions: {size}
- Style: {style}
- Include number/count: {include_number}
- AI visual elements: {ai_visual_elements}
- High contrast: {high_contrast}

DESIGN OBJECTIVES:
1. Create a thumbnail that maximizes click-through rate
2. Ensure text is readable at small sizes (mobile view)
3. Use bold, attention-grabbing visual elements
4. Incorporate AI/tech visual themes if relevant
5. Maintain high contrast for visibility
6. Follow YouTube thumbnail best practices

Focus on creating a design that:
- Stands out in a crowded feed of videos
- Clearly communicates the video's value proposition
- Uses psychological triggers to encourage clicks
- Remains readable and appealing at thumbnail size
- Aligns with current design trends and best practices

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_list_graphics_prompt(self, task: Task, inputs: Dict[str, Any], 
                                        requirements: Dict[str, Any]) -> str:
        """Build prompt for list graphics and visual cards"""
        card_count = requirements.get('card_count', 7)
        consistent_design = requirements.get('consistent_design', True)
        include_logos = requirements.get('include_logos', True)
        ranking_numbers = requirements.get('ranking_numbers', True)
        
        schema = {
            "list_graphics_system": {
                "design_concept": "string - overall visual theme for the list",
                "card_template": {
                    "layout_structure": "string - how each card is organized",
                    "dimensions": "string - size of each individual card",
                    "background_style": "string - background design approach",
                    "border_treatment": "string - how borders/edges are handled"
                },
                "visual_consistency": {
                    "color_palette": ["string - colors used across all cards"],
                    "typography_system": "string - font choices and hierarchy",
                    "spacing_grid": "string - consistent spacing system",
                    "visual_style": "string - overall aesthetic approach"
                }
            },
            "individual_cards": [
                {
                    "card_number": "number - position in list (1-N)",
                    "content_area": "string - space for main content/text",
                    "ranking_display": "string - how the number/rank is shown",
                    "logo_placement": "string - where logos/icons go" if include_logos else None,
                    "visual_hierarchy": "string - how elements are prioritized",
                    "unique_elements": "string - what makes this card distinct"
                }
            ],
            "design_specifications": {
                "total_cards": "number - how many cards in the set",
                "export_formats": ["string - file formats needed"],
                "usage_context": "string - where these will be used",
                "scalability": "string - how they work at different sizes"
            },
            "branding_elements": {
                "brand_consistency": "string - how to maintain brand identity",
                "color_coding": "string - if different categories use different colors",
                "iconography": "string - icon style and usage",
                "call_to_action": "string - any CTA elements to include"
            }
        }
        
        return f"""Design Task: Create a cohesive set of list graphics/visual cards

USER REQUEST: {inputs.get('user_request', 'Create list graphics')}
TASK: {task.task_name}

LIST GRAPHICS REQUIREMENTS:
- Number of cards: {card_count}
- Consistent design: {consistent_design}
- Include logos/icons: {include_logos}
- Show ranking numbers: {ranking_numbers}

DESIGN OBJECTIVES:
1. Create a visually cohesive set of graphics that work together
2. Ensure each card is readable and informative
3. Design for social media sharing and video use
4. Maintain visual hierarchy and clear information display
5. Create templates that can be easily updated with new content

Focus on creating graphics that:
- Work well both individually and as a complete set
- Are optimized for digital display and social sharing
- Clearly communicate ranking/priority through visual design
- Maintain professional quality and brand consistency
- Can be easily reproduced for future content

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_social_assets_prompt(self, task: Task, inputs: Dict[str, Any], 
                                        requirements: Dict[str, Any]) -> str:
        """Build prompt for social media assets"""
        platforms = requirements.get('platforms', ['twitter', 'linkedin', 'instagram'])
        teaser_style = requirements.get('teaser_style', True)
        include_top_3_preview = requirements.get('include_top_3_preview', True)
        
        schema = {
            "social_media_assets": {
                "campaign_concept": "string - overarching theme for social promotion",
                "platform_specific_designs": [
                    {
                        "platform": "string - social media platform name",
                        "dimensions": "string - optimal size for this platform",
                        "design_approach": "string - platform-specific design strategy",
                        "content_focus": "string - what to emphasize for this audience",
                        "engagement_strategy": "string - how to maximize engagement"
                    }
                ],
                "visual_elements": {
                    "preview_content": "string - how to tease the main content",
                    "branding_elements": "string - logo, colors, fonts to include",
                    "call_to_action": "string - what action you want users to take",
                    "hashtag_integration": "string - how to incorporate relevant hashtags"
                }
            },
            "content_strategy": {
                "teaser_approach": "string - how to create curiosity without giving everything away",
                "value_proposition": "string - why users should engage with full content",
                "social_proof": "string - elements that build credibility",
                "urgency_factors": "string - time-sensitive elements to include"
            },
            "technical_specifications": {
                "file_formats": ["string - formats needed for each platform"],
                "quality_settings": "string - resolution and compression guidelines",
                "accessibility": "string - alt text and accessibility considerations",
                "mobile_optimization": "string - how designs work on mobile devices"
            }
        }
        
        return f"""Design Task: Create social media promotional assets

USER REQUEST: {inputs.get('user_request', 'Create social assets')}
TASK: {task.task_name}

SOCIAL ASSETS REQUIREMENTS:
- Target platforms: {', '.join(platforms)}
- Teaser style: {teaser_style}
- Include top 3 preview: {include_top_3_preview}

DESIGN OBJECTIVES:
1. Create platform-optimized graphics that drive traffic to main content
2. Design engaging visuals that encourage shares and comments
3. Maintain brand consistency across all platforms
4. Include clear calls-to-action that guide user behavior
5. Optimize for both desktop and mobile viewing

Focus on creating assets that:
- Capture attention in busy social media feeds
- Provide enough value to encourage engagement
- Drive traffic back to the main content
- Work effectively across different platform algorithms
- Encourage social sharing and viral potential

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_design_prompt(self, task: Task, inputs: Dict[str, Any], 
                                         requirements: Dict[str, Any]) -> str:
        """Build prompt for general design tasks"""
        style = requirements.get('style', 'professional')
        include_text = requirements.get('include_text', False)
        brand_colors = requirements.get('brand_colors', True)
        
        schema = {
            "design_concept": {
                "visual_theme": "string - overall design theme and approach",
                "target_audience": "string - who this design is intended for",
                "primary_message": "string - main message to communicate",
                "emotional_tone": "string - feeling the design should evoke"
            },
            "design_elements": {
                "layout": "string - how elements are arranged",
                "color_scheme": {
                    "primary_colors": ["string - main colors"],
                    "secondary_colors": ["string - supporting colors"],
                    "color_psychology": "string - why these colors were chosen"
                },
                "typography": {
                    "font_choices": "string - typefaces to use",
                    "text_hierarchy": "string - how text is organized",
                    "readability": "string - ensuring text is clear"
                } if include_text else None,
                "imagery": "string - photographic or illustrative elements",
                "graphics": "string - icons, shapes, decorative elements"
            },
            "technical_details": {
                "dimensions": "string - size specifications",
                "file_format": "string - recommended output format",
                "resolution": "string - quality specifications",
                "usage_context": "string - where/how this will be used"
            }
        }
        
        return f"""Design Task: Create high-quality visual design

USER REQUEST: {inputs.get('user_request', 'Create design')}
TASK: {task.task_name}

DESIGN REQUIREMENTS:
- Style: {style}
- Include text: {include_text}
- Use brand colors: {brand_colors}

DESIGN OBJECTIVES:
1. Create visually appealing design that serves its intended purpose
2. Ensure design aligns with brand identity and guidelines
3. Optimize for the specific use case and platform
4. Maintain professional quality and attention to detail
5. Consider accessibility and inclusive design principles

Focus on creating a design that:
- Effectively communicates the intended message
- Appeals to the target audience
- Functions well in its intended context
- Maintains high professional standards
- Can be easily implemented and reproduced

{self._build_json_schema_prompt(schema)}"""
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for design output validation"""
        return ['design_concept', 'visual_elements']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate design output format"""
        # Check for main design structure
        design_fields = ['thumbnail_design', 'list_graphics_system', 'social_media_assets', 'design_concept']
        has_design_content = any(field in outputs for field in design_fields)
        
        if not has_design_content:
            return False
        
        # Validate that design specifications exist
        spec_fields = ['design_specifications', 'technical_specifications', 'technical_details']
        has_specifications = any(field in outputs for field in spec_fields)
        
        return has_specifications
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback design output"""
        user_request = inputs.get('user_request', 'design creation')
        size = requirements.get('size', '1200x630')
        style = requirements.get('style', 'professional')
        
        return {
            'design_concept': {
                'visual_theme': f'Professional design for {user_request}',
                'target_audience': 'General audience',
                'primary_message': f'Visual content related to {user_request}',
                'emotional_tone': 'Professional and engaging'
            },
            'design_elements': {
                'layout': 'Clean, organized layout with clear hierarchy',
                'color_scheme': {
                    'primary_colors': ['#2563eb', '#ffffff'],
                    'secondary_colors': ['#64748b', '#f1f5f9'],
                    'color_psychology': 'Blue for trust and professionalism'
                },
                'imagery': f'Relevant imagery for {user_request}',
                'graphics': 'Minimal, clean graphic elements'
            },
            'technical_details': {
                'dimensions': size,
                'file_format': 'PNG',
                'resolution': '300 DPI',
                'usage_context': f'Digital use for {task.task_name}'
            },
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return design agent specializations"""
        return [
            "YouTube thumbnail design",
            "Social media graphics",
            "List and ranking visuals", 
            "Brand identity design",
            "Digital marketing assets",
            "UI/UX design elements",
            "Infographic creation",
            "Platform-specific optimization"
        ]
