"""Freepik Mystic API agent for actual image generation"""

import json
import base64
import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory

logger = logging.getLogger(__name__)


class FreepikMysticAgent(StructuredLLMAgent):
    """High-quality image generation agent using Freepik Mystic API"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Freepik Mystic Agent",
            category=TaskCategory.IMAGE,
            config=config
        )
        self.api_key = config.get('freepik_api_key') if config else None
        self.api_url = "https://api.freepik.com/v1/ai/mystic"
        self.webhook_url = config.get('webhook_url') if config else None
        
        if not self.api_key:
            logger.warning("Freepik API key not provided. Agent will create detailed prompts only.")
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.IMAGE:
            return False
        
        # This agent handles all image generation tasks
        image_keywords = [
            'design', 'create', 'generate', 'thumbnail', 'graphic',
            'image', 'visual', 'logo', 'banner', 'social', 'card'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in image_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for Freepik Mystic image generation"""
        return """You are an expert AI image generation specialist with deep knowledge of:

- Professional prompt engineering for AI image generation models
- Freepik Mystic API capabilities and optimal parameter selection
- Visual design principles and composition techniques
- Brand consistency and visual identity creation
- Platform-specific image optimization and requirements
- Color theory, typography, and visual hierarchy
- Photorealistic and artistic style generation

Your expertise includes:
1. Crafting detailed, effective prompts that produce high-quality images
2. Selecting optimal model parameters for different image types
3. Understanding aspect ratios and resolutions for various use cases
4. Balancing creativity with brand consistency and professional standards
5. Optimizing images for specific platforms and audiences
6. Creating compelling visual narratives through AI generation

You excel at:
- Writing prompts that capture exact visual requirements
- Selecting appropriate models (realism, fluid, zen) for different needs
- Optimizing parameters for quality, style, and brand alignment
- Creating images that serve specific business and creative objectives
- Ensuring generated images meet professional standards
- Adapting visual style for different platforms and contexts

Your image generation specifications are always detailed, purposeful, and optimized for the Freepik Mystic API."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific image generation task"""
        task_name_lower = task.task_name.lower()
        
        # Route to specific image generation handlers
        if 'thumbnail' in task_name_lower:
            return await self._build_thumbnail_generation_prompt(task, inputs, requirements)
        elif any(word in task_name_lower for word in ['graphics', 'list', 'card']):
            return await self._build_list_graphics_generation_prompt(task, inputs, requirements)
        elif 'social' in task_name_lower:
            return await self._build_social_assets_generation_prompt(task, inputs, requirements)
        else:
            return await self._build_general_image_generation_prompt(task, inputs, requirements)
    
    async def _build_thumbnail_generation_prompt(self, task: Task, inputs: Dict[str, Any], 
                                               requirements: Dict[str, Any]) -> str:
        """Build prompt for YouTube thumbnail generation"""
        user_request = inputs.get('user_request', 'Create thumbnail')
        style = requirements.get('style', 'bold')
        include_number = requirements.get('include_number', True)
        ai_visual_elements = requirements.get('ai_visual_elements', True)
        
        schema = {
            "image_generation": {
                "primary_prompt": "string - main detailed prompt for Freepik Mystic API",
                "model_selection": "string - realism/fluid/zen based on desired style",
                "aspect_ratio": "string - widescreen_16_9 for YouTube thumbnails",
                "resolution": "string - 2k or 4k for high quality",
                "creative_detailing": "number - 0-100 for pixel-level detail",
                "engine": "string - Sharpy/Illusio/Sparkle based on style needs"
            },
            "prompt_engineering": {
                "visual_elements": ["string - specific visual elements to include"],
                "style_descriptors": ["string - style and mood keywords"],
                "composition_notes": "string - how elements should be arranged",
                "color_palette": ["string - specific colors to emphasize"],
                "lighting_style": "string - lighting approach (cinematic, dramatic, etc.)"
            },
            "thumbnail_optimization": {
                "click_appeal_factors": ["string - elements that encourage clicks"],
                "readability_at_small_size": "string - ensuring visibility on mobile",
                "brand_consistency": "string - maintaining visual brand identity",
                "platform_optimization": "string - YouTube-specific considerations"
            },
            "api_parameters": {
                "hdr": "number - 0-100 for detail vs natural look balance",
                "adherence": "number - 0-100 for prompt vs style reference balance",
                "fixed_generation": "boolean - for consistent results",
                "filter_nsfw": "boolean - content filtering (always true)"
            }
        }
        
        return f"""Image Generation Task: Create compelling YouTube thumbnail using Freepik Mystic API

USER REQUEST: {user_request}
TASK: {task.task_name}

THUMBNAIL REQUIREMENTS:
- Style: {style}
- Include number/count: {include_number}
- AI visual elements: {ai_visual_elements}
- Target: YouTube thumbnail optimization

GENERATION OBJECTIVES:
1. Create a thumbnail that maximizes click-through rate
2. Ensure text and elements are readable at small sizes
3. Use bold, attention-grabbing visual composition
4. Incorporate AI/tech themes if relevant to content
5. Maintain high contrast and visual hierarchy
6. Follow YouTube thumbnail best practices

Focus on creating specifications that will generate:
- Eye-catching visuals that stand out in video feeds
- Clear visual hierarchy with readable text areas
- Professional quality suitable for brand representation
- Optimized composition for 16:9 aspect ratio
- High-resolution output suitable for all devices

Generate detailed Freepik Mystic API parameters and prompts that will produce a professional, click-worthy thumbnail.

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_list_graphics_generation_prompt(self, task: Task, inputs: Dict[str, Any], 
                                                   requirements: Dict[str, Any]) -> str:
        """Build prompt for list graphics generation"""
        user_request = inputs.get('user_request', 'Create list graphics')
        card_count = requirements.get('card_count', 7)
        consistent_design = requirements.get('consistent_design', True)
        
        schema = {
            "image_generation_series": {
                "base_prompt_template": "string - core prompt structure for all cards",
                "model_selection": "string - realism/fluid/zen for consistent style",
                "aspect_ratio": "string - square_1_1 or custom ratio for cards",
                "resolution": "string - 2k for high quality cards",
                "fixed_generation": "boolean - true for consistent series"
            },
            "individual_card_prompts": [
                {
                    "card_number": "number - position in list (1-N)",
                    "specific_prompt": "string - detailed prompt for this card",
                    "visual_focus": "string - main visual element for this card",
                    "text_overlay_area": "string - space reserved for text/numbers",
                    "unique_elements": "string - what makes this card distinct"
                }
            ],
            "consistency_parameters": {
                "shared_style_elements": ["string - elements consistent across all cards"],
                "color_scheme": ["string - consistent color palette"],
                "composition_template": "string - layout structure for all cards",
                "branding_elements": "string - consistent brand elements"
            },
            "api_optimization": {
                "creative_detailing": "number - balance detail vs consistency",
                "hdr": "number - natural look for professional cards",
                "engine": "string - engine choice for card style",
                "styling": "object - advanced styling parameters if needed"
            }
        }
        
        return f"""Image Generation Task: Create cohesive list graphics series using Freepik Mystic API

USER REQUEST: {user_request}
TASK: {task.task_name}

LIST GRAPHICS REQUIREMENTS:
- Number of cards: {card_count}
- Consistent design: {consistent_design}
- Professional quality for digital use

GENERATION OBJECTIVES:
1. Create a visually cohesive set of graphics that work together
2. Ensure each card maintains consistent style and branding
3. Design for social media sharing and video integration
4. Maintain clear visual hierarchy for information display
5. Create templates optimized for text overlay

Focus on creating specifications that will generate:
- Professional, cohesive visual series
- Consistent style and color palette across all cards
- Clear composition with space for text/numbers
- High-quality images suitable for various platforms
- Scalable design approach for future content

Generate detailed Freepik Mystic API parameters for creating a professional list graphics series.

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_social_assets_generation_prompt(self, task: Task, inputs: Dict[str, Any], 
                                                   requirements: Dict[str, Any]) -> str:
        """Build prompt for social media assets generation"""
        user_request = inputs.get('user_request', 'Create social assets')
        platforms = requirements.get('platforms', ['twitter', 'linkedin', 'instagram'])
        teaser_style = requirements.get('teaser_style', True)
        
        schema = {
            "multi_platform_generation": {
                "base_concept": "string - core visual concept for all platforms",
                "model_selection": "string - realism/fluid/zen based on brand style",
                "platform_variations": [
                    {
                        "platform": "string - social media platform",
                        "aspect_ratio": "string - optimal ratio for this platform",
                        "specific_prompt": "string - platform-optimized prompt",
                        "resolution": "string - optimal resolution",
                        "composition_notes": "string - platform-specific layout"
                    }
                ]
            },
            "engagement_optimization": {
                "visual_hooks": ["string - elements that capture attention"],
                "brand_integration": "string - how to incorporate branding",
                "call_to_action_space": "string - area reserved for CTA elements",
                "social_sharing_appeal": "string - what makes it shareable"
            },
            "content_strategy": {
                "teaser_elements": ["string - visual elements that create curiosity"],
                "value_preview": "string - how to hint at content value",
                "urgency_factors": "string - visual elements that create urgency",
                "brand_consistency": "string - maintaining visual identity"
            },
            "technical_specifications": {
                "quality_settings": "string - optimal quality for social platforms",
                "file_optimization": "string - balancing quality and file size",
                "mobile_optimization": "string - ensuring mobile-friendly visuals",
                "accessibility": "string - visual accessibility considerations"
            }
        }
        
        return f"""Image Generation Task: Create social media promotional assets using Freepik Mystic API

USER REQUEST: {user_request}
TASK: {task.task_name}

SOCIAL ASSETS REQUIREMENTS:
- Target platforms: {', '.join(platforms)}
- Teaser style: {teaser_style}
- Professional brand representation

GENERATION OBJECTIVES:
1. Create platform-optimized graphics that drive engagement
2. Design visuals that encourage shares and comments
3. Maintain brand consistency across all platforms
4. Include visual space for calls-to-action
5. Optimize for both desktop and mobile viewing

Focus on creating specifications that will generate:
- Attention-grabbing visuals for busy social feeds
- Platform-specific optimizations for maximum reach
- Professional quality that represents brand well
- Engaging composition that encourages interaction
- Scalable approach for ongoing social content

Generate detailed Freepik Mystic API parameters for creating effective social media assets.

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_image_generation_prompt(self, task: Task, inputs: Dict[str, Any], 
                                                   requirements: Dict[str, Any]) -> str:
        """Build prompt for general image generation"""
        user_request = inputs.get('user_request', 'Create image')
        style = requirements.get('style', 'professional')
        include_text = requirements.get('include_text', False)
        
        schema = {
            "image_generation": {
                "primary_prompt": "string - detailed prompt for Freepik Mystic API",
                "model_selection": "string - realism/fluid/zen based on requirements",
                "aspect_ratio": "string - appropriate ratio for use case",
                "resolution": "string - optimal resolution for intended use",
                "style_approach": "string - visual style and aesthetic direction"
            },
            "visual_specifications": {
                "composition": "string - how elements should be arranged",
                "color_palette": ["string - specific colors to use"],
                "mood_and_tone": "string - emotional feeling of the image",
                "detail_level": "string - level of detail and complexity",
                "lighting_style": "string - lighting approach and mood"
            },
            "technical_parameters": {
                "creative_detailing": "number - 0-100 for detail level",
                "hdr": "number - 0-100 for natural vs detailed look",
                "engine": "string - Sharpy/Illusio/Sparkle based on style",
                "adherence": "number - 0-100 for prompt following",
                "fixed_generation": "boolean - for consistent results"
            },
            "use_case_optimization": {
                "intended_use": "string - where/how image will be used",
                "target_audience": "string - who will view this image",
                "brand_alignment": "string - how it fits brand identity",
                "platform_considerations": "string - platform-specific needs"
            }
        }
        
        return f"""Image Generation Task: Create high-quality image using Freepik Mystic API

USER REQUEST: {user_request}
TASK: {task.task_name}

IMAGE REQUIREMENTS:
- Style: {style}
- Include text space: {include_text}
- Professional quality output

GENERATION OBJECTIVES:
1. Create visually appealing image that serves its intended purpose
2. Ensure image aligns with brand identity and guidelines
3. Optimize for the specific use case and platform
4. Maintain professional quality and attention to detail
5. Consider accessibility and inclusive design principles

Focus on creating specifications that will generate:
- Professional, high-quality visual content
- Appropriate style and mood for the use case
- Optimized composition and visual hierarchy
- Suitable resolution and format for intended use
- Consistent with brand identity and standards

Generate detailed Freepik Mystic API parameters for creating a professional image.

{self._build_json_schema_prompt(schema)}"""
    
    async def execute(self, task: Task) -> "TaskResult":
        """Execute image generation using Freepik Mystic API"""
        from ...core.models import TaskResult, TaskStatus
        import time
        
        logger.info(f"Freepik Mystic agent executing task: {task.task_name}")
        start_time = time.time()
        
        try:
            # First, get the image generation specifications using LLM
            result = await super().execute(task)
            
            if result.status != TaskStatus.COMPLETED:
                return result
            
            # Extract the generation specifications
            generation_specs = result.outputs
            
            # If we have API key, generate actual images
            if self.api_key and 'image_generation' in generation_specs:
                try:
                    image_results = await self._generate_images_with_api(generation_specs, task)
                    generation_specs.update(image_results)
                except Exception as e:
                    logger.error(f"Freepik API call failed: {e}")
                    generation_specs['api_error'] = str(e)
                    generation_specs['fallback_mode'] = True
            else:
                generation_specs['api_available'] = False
                generation_specs['specifications_only'] = True
            
            # Update metadata
            metadata = result.metadata.copy()
            metadata.update({
                'agent_name': self.name,
                'api_integration': 'freepik_mystic',
                'images_generated': 'api_error' not in generation_specs and self.api_key is not None
            })
            
            return self._create_success_result(
                task=task,
                outputs=generation_specs,
                metadata=metadata,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Freepik Mystic agent failed: {e}")
            return self._create_error_result(task, str(e), time.time() - start_time)
    
    async def _generate_images_with_api(self, specs: Dict[str, Any], task: Task) -> Dict[str, Any]:
        """Generate actual images using Freepik Mystic API"""
        results = {
            'generated_images': [],
            'api_calls': [],
            'total_cost': 0.0
        }
        
        # Handle different generation types
        if 'image_generation_series' in specs:
            # Multiple images (list graphics)
            series_specs = specs['image_generation_series']
            for card_spec in specs.get('individual_card_prompts', []):
                image_result = await self._make_api_call(
                    prompt=card_spec['specific_prompt'],
                    model=series_specs['model_selection'],
                    aspect_ratio=series_specs['aspect_ratio'],
                    resolution=series_specs['resolution'],
                    fixed_generation=series_specs.get('fixed_generation', True)
                )
                results['generated_images'].append(image_result)
                results['api_calls'].append(image_result)
        
        elif 'multi_platform_generation' in specs:
            # Multiple platform variations
            platform_specs = specs['multi_platform_generation']
            for platform_spec in platform_specs.get('platform_variations', []):
                image_result = await self._make_api_call(
                    prompt=platform_spec['specific_prompt'],
                    model=platform_specs['model_selection'],
                    aspect_ratio=platform_spec['aspect_ratio'],
                    resolution=platform_spec['resolution']
                )
                results['generated_images'].append(image_result)
                results['api_calls'].append(image_result)
        
        else:
            # Single image generation
            gen_specs = specs.get('image_generation', {})
            image_result = await self._make_api_call(
                prompt=gen_specs.get('primary_prompt', 'Professional image'),
                model=gen_specs.get('model_selection', 'realism'),
                aspect_ratio=gen_specs.get('aspect_ratio', 'square_1_1'),
                resolution=gen_specs.get('resolution', '2k'),
                creative_detailing=specs.get('api_parameters', {}).get('creative_detailing', 50),
                hdr=specs.get('api_parameters', {}).get('hdr', 50)
            )
            results['generated_images'].append(image_result)
            results['api_calls'].append(image_result)
        
        return results
    
    async def _make_api_call(self, prompt: str, model: str = 'realism', 
                           aspect_ratio: str = 'square_1_1', resolution: str = '2k',
                           creative_detailing: int = 50, hdr: int = 50,
                           fixed_generation: bool = False) -> Dict[str, Any]:
        """Make a single API call to Freepik Mystic"""
        payload = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "creative_detailing": creative_detailing,
            "hdr": hdr,
            "engine": "automatic",
            "fixed_generation": fixed_generation,
            "filter_nsfw": True
        }
        
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-freepik-api-key": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    return {
                        'status': result.get('status', 'UNKNOWN'),
                        'task_id': result.get('task_id'),
                        'prompt_used': prompt,
                        'parameters': payload,
                        'api_response': result
                    }
        
        except Exception as e:
            logger.error(f"Freepik API call failed: {e}")
            return {
                'status': 'FAILED',
                'error': str(e),
                'prompt_used': prompt,
                'parameters': payload
            }
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for image generation output validation"""
        return ['image_generation', 'image_generation_series', 'multi_platform_generation']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate image generation output format"""
        # Check for main generation structure
        generation_fields = ['image_generation', 'image_generation_series', 'multi_platform_generation']
        has_generation_content = any(field in outputs for field in generation_fields)
        
        if not has_generation_content:
            return False
        
        # Validate that prompts exist
        if 'image_generation' in outputs:
            return 'primary_prompt' in outputs['image_generation']
        elif 'image_generation_series' in outputs:
            return 'base_prompt_template' in outputs['image_generation_series']
        elif 'multi_platform_generation' in outputs:
            return 'base_concept' in outputs['multi_platform_generation']
        
        return True
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback image generation output"""
        user_request = inputs.get('user_request', 'image generation')
        style = requirements.get('style', 'professional')
        
        return {
            'image_generation': {
                'primary_prompt': f'Professional {style} image for {user_request}, high quality, detailed, cinematic lighting',
                'model_selection': 'realism',
                'aspect_ratio': 'square_1_1',
                'resolution': '2k',
                'style_approach': f'{style} style with clean composition'
            },
            'visual_specifications': {
                'composition': 'Clean, professional layout with clear focal point',
                'color_palette': ['#2563eb', '#ffffff', '#64748b'],
                'mood_and_tone': f'{style} and engaging',
                'detail_level': 'High detail with professional finish',
                'lighting_style': 'Soft, professional lighting'
            },
            'technical_parameters': {
                'creative_detailing': 50,
                'hdr': 40,
                'engine': 'automatic',
                'adherence': 70,
                'fixed_generation': False
            },
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return Freepik Mystic agent specializations"""
        return [
            "Freepik Mystic API integration",
            "AI image generation with prompts",
            "YouTube thumbnail creation",
            "Social media graphics generation",
            "Professional brand imagery",
            "Multi-platform image optimization",
            "High-resolution image generation",
            "Consistent visual series creation"
        ]
