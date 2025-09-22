"""Video agent for high-quality video editing and compilation"""

import json
from typing import Dict, Any, List
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory


class VideoAgent(StructuredLLMAgent):
    """High-quality video agent for editing, compilation, and optimization"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Video Agent",
            category=TaskCategory.VIDEO,
            config=config
        )
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.VIDEO:
            return False
        
        video_keywords = [
            'video', 'edit', 'compile', 'render', 'montage', 'clip',
            'short', 'reel', 'story', 'optimize', 'export', 'cut'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in video_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for video tasks"""
        return """You are an expert video editor and post-production specialist with extensive experience in:

- Professional video editing and post-production workflows
- Multi-platform video optimization and formatting
- Motion graphics and visual effects integration
- Color grading and visual consistency
- Audio-visual synchronization and mixing
- Social media and digital platform requirements
- Video compression and quality optimization
- Accessibility and caption integration

Your expertise includes:
1. Creating engaging video narratives and pacing
2. Optimizing content for different platforms and audiences
3. Integrating graphics, text, and visual elements seamlessly
4. Managing technical specifications and quality standards
5. Creating efficient workflows for content production
6. Ensuring accessibility and inclusive video design
7. Balancing quality with file size and platform requirements

You excel at:
- Crafting compelling video sequences that maintain viewer engagement
- Optimizing videos for platform-specific algorithms and requirements
- Creating smooth transitions and professional visual flow
- Integrating multiple media elements into cohesive productions
- Managing technical aspects while maintaining creative vision
- Ensuring consistent branding and visual identity
- Meeting accessibility standards and inclusive design principles

Your video productions are always professional, engaging, and optimized for their intended platform and audience."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific video task"""
        task_name_lower = task.task_name.lower()
        
        # Route to specific video task handlers
        if 'main' in task_name_lower or 'edit' in task_name_lower:
            return await self._build_main_video_prompt(task, inputs, requirements)
        elif 'short' in task_name_lower or 'clip' in task_name_lower:
            return await self._build_short_clips_prompt(task, inputs, requirements)
        elif 'optimize' in task_name_lower or 'platform' in task_name_lower:
            return await self._build_platform_optimization_prompt(task, inputs, requirements)
        else:
            return await self._build_general_video_prompt(task, inputs, requirements)
    
    async def _build_main_video_prompt(self, task: Task, inputs: Dict[str, Any], 
                                     requirements: Dict[str, Any]) -> str:
        """Build prompt for main video editing and compilation"""
        style = requirements.get('style', 'dynamic')
        include_animations = requirements.get('include_animations', True)
        smooth_transitions = requirements.get('smooth_transitions', True)
        on_screen_text = requirements.get('on_screen_text', True)
        duration = requirements.get('duration', '8-12 minutes')
        
        schema = {
            "video_structure": {
                "opening_sequence": {
                    "duration": "string - length of opening",
                    "visual_style": "string - opening visual approach",
                    "hook_strategy": "string - how to capture attention immediately",
                    "branding_elements": "string - logo, title, channel branding"
                },
                "main_content_sections": [
                    {
                        "section_number": "number - order in video",
                        "title": "string - section title/topic",
                        "duration": "string - estimated length",
                        "visual_approach": "string - how to present this section visually",
                        "key_graphics": ["string - graphics/images needed"],
                        "text_overlays": ["string - on-screen text elements"],
                        "transition_in": "string - how to transition into this section",
                        "transition_out": "string - how to transition out of this section"
                    }
                ],
                "closing_sequence": {
                    "duration": "string - length of closing",
                    "call_to_action": "string - what viewers should do next",
                    "end_screen_elements": ["string - subscribe, related videos, etc."],
                    "branding_outro": "string - consistent closing branding"
                }
            },
            "visual_design": {
                "overall_style": "string - consistent visual theme",
                "color_palette": ["string - primary colors used throughout"],
                "typography": {
                    "title_fonts": "string - fonts for main titles",
                    "body_fonts": "string - fonts for body text",
                    "text_animation": "string - how text appears/animates"
                },
                "graphic_elements": {
                    "lower_thirds": "string - name/title graphics style",
                    "bullet_points": "string - how to display lists visually",
                    "progress_indicators": "string - showing progress through content",
                    "background_graphics": "string - subtle background elements"
                }
            },
            "animation_and_effects": {
                "transition_types": ["string - types of transitions between sections"],
                "text_animations": ["string - how text enters and exits"],
                "graphic_animations": ["string - how graphics move and appear"],
                "camera_movements": ["string - zoom, pan, tilt effects"],
                "timing_and_pacing": "string - rhythm of animations and cuts"
            },
            "technical_specifications": {
                "resolution": "string - video resolution (1080p, 4K, etc.)",
                "frame_rate": "string - frames per second",
                "aspect_ratio": "string - width:height ratio",
                "codec": "string - video compression format",
                "bitrate": "string - quality vs file size balance",
                "audio_sync": "string - ensuring perfect audio-video alignment"
            }
        }
        
        return f"""Video Task: Create main video edit and compilation

USER REQUEST: {inputs.get('user_request', 'Create main video')}
TASK: {task.task_name}

VIDEO REQUIREMENTS:
- Style: {style}
- Include animations: {include_animations}
- Smooth transitions: {smooth_transitions}
- On-screen text: {on_screen_text}
- Duration: {duration}

VIDEO OBJECTIVES:
1. Create engaging video that maintains viewer attention throughout
2. Ensure professional quality and smooth visual flow
3. Integrate all content elements seamlessly
4. Optimize for platform algorithms and engagement
5. Maintain consistent branding and visual identity

Focus on creating a video that:
- Captures attention immediately and maintains engagement
- Uses professional editing techniques and smooth transitions
- Integrates graphics, text, and visual elements effectively
- Maintains consistent pacing and energy throughout
- Ends with clear call-to-action and next steps

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_short_clips_prompt(self, task: Task, inputs: Dict[str, Any], 
                                      requirements: Dict[str, Any]) -> str:
        """Build prompt for short-form video clips"""
        clip_count = requirements.get('clip_count', 3)
        duration = requirements.get('duration', '60 seconds')
        vertical_format = requirements.get('vertical_format', True)
        highlight_top_3 = requirements.get('highlight_top_3', True)
        engaging_hooks = requirements.get('engaging_hooks', True)
        
        schema = {
            "short_clips_strategy": {
                "content_selection": {
                    "clip_topics": ["string - what each clip will focus on"],
                    "hook_strategies": ["string - how to grab attention in first 3 seconds"],
                    "value_propositions": ["string - why viewers should watch each clip"],
                    "viral_elements": ["string - elements that encourage sharing"]
                },
                "format_optimization": {
                    "aspect_ratio": "string - 9:16 for vertical, 16:9 for horizontal",
                    "safe_zones": "string - areas to keep important content",
                    "text_sizing": "string - ensuring readability on mobile",
                    "visual_hierarchy": "string - organizing elements for small screens"
                }
            },
            "individual_clips": [
                {
                    "clip_number": "number - order/priority",
                    "hook": "string - attention-grabbing opening (0-3 seconds)",
                    "main_content": "string - core message/value (3-45 seconds)",
                    "call_to_action": "string - what viewer should do (45-60 seconds)",
                    "visual_style": "string - specific visual approach for this clip",
                    "text_overlays": ["string - key text elements"],
                    "music_style": "string - background music approach",
                    "pacing": "string - fast/medium/slow editing rhythm"
                }
            ],
            "engagement_optimization": {
                "retention_tactics": ["string - techniques to keep viewers watching"],
                "interaction_prompts": ["string - encouraging likes, comments, shares"],
                "algorithm_optimization": ["string - elements that boost platform reach"],
                "accessibility_features": ["string - captions, visual descriptions"]
            },
            "technical_requirements": {
                "resolution": "string - optimal resolution for platform",
                "file_size": "string - maximum file size constraints",
                "compression": "string - quality vs size optimization",
                "thumbnail_frames": ["string - which frames work best as thumbnails"],
                "export_settings": "string - specific export parameters"
            }
        }
        
        return f"""Video Task: Create engaging short-form video clips

USER REQUEST: {inputs.get('user_request', 'Create short clips')}
TASK: {task.task_name}

SHORT CLIPS REQUIREMENTS:
- Number of clips: {clip_count}
- Duration: {duration}
- Vertical format: {vertical_format}
- Highlight top content: {highlight_top_3}
- Engaging hooks: {engaging_hooks}

VIDEO OBJECTIVES:
1. Create highly engaging short-form content optimized for social platforms
2. Maximize viewer retention and engagement within time constraints
3. Encourage sharing and viral potential
4. Drive traffic back to main content or channel
5. Optimize for platform-specific algorithms and features

Focus on creating clips that:
- Hook viewers immediately in the first 3 seconds
- Deliver maximum value in minimal time
- Use platform-specific best practices and formats
- Encourage interaction and engagement
- Work effectively on mobile devices

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_platform_optimization_prompt(self, task: Task, inputs: Dict[str, Any], 
                                                 requirements: Dict[str, Any]) -> str:
        """Build prompt for platform-specific video optimization"""
        platforms = requirements.get('platforms', ['youtube', 'tiktok', 'instagram'])
        quality_settings = requirements.get('quality_settings', 'high')
        include_captions = requirements.get('include_captions', True)
        seo_tags = requirements.get('seo_tags', True)
        
        schema = {
            "platform_specifications": [
                {
                    "platform": "string - platform name",
                    "optimal_specs": {
                        "resolution": "string - best resolution for this platform",
                        "aspect_ratio": "string - required aspect ratio",
                        "duration_limits": "string - minimum and maximum length",
                        "file_size_limit": "string - maximum file size",
                        "frame_rate": "string - optimal frame rate"
                    },
                    "algorithm_optimization": {
                        "engagement_signals": ["string - what the algorithm prioritizes"],
                        "retention_factors": ["string - what keeps videos in feed"],
                        "discovery_optimization": ["string - how to improve discoverability"],
                        "timing_strategies": ["string - when to post for best reach"]
                    },
                    "content_adaptations": {
                        "thumbnail_requirements": "string - thumbnail specs and best practices",
                        "title_optimization": "string - how to optimize titles for this platform",
                        "description_strategy": "string - description best practices",
                        "hashtag_strategy": "string - hashtag usage for discovery"
                    }
                }
            ],
            "accessibility_features": {
                "caption_specifications": {
                    "caption_style": "string - font, size, color for captions",
                    "positioning": "string - where captions appear on screen",
                    "timing": "string - caption timing and duration",
                    "language_support": ["string - languages to support"]
                },
                "visual_accessibility": {
                    "color_contrast": "string - ensuring sufficient contrast",
                    "text_readability": "string - font sizes and clarity",
                    "motion_considerations": "string - avoiding problematic motion"
                }
            },
            "seo_and_discovery": {
                "keyword_optimization": ["string - relevant keywords for each platform"],
                "metadata_strategy": "string - how to optimize video metadata",
                "thumbnail_seo": "string - optimizing thumbnails for discovery",
                "cross_platform_strategy": "string - how versions work together"
            },
            "quality_management": {
                "compression_settings": "string - balancing quality and file size",
                "backup_versions": ["string - additional quality versions to create"],
                "quality_assurance": ["string - checks to perform before publishing"],
                "version_control": "string - managing different platform versions"
            }
        }
        
        return f"""Video Task: Optimize video for multiple platforms

USER REQUEST: {inputs.get('user_request', 'Optimize for platforms')}
TASK: {task.task_name}

PLATFORM OPTIMIZATION REQUIREMENTS:
- Target platforms: {', '.join(platforms)}
- Quality settings: {quality_settings}
- Include captions: {include_captions}
- SEO optimization: {seo_tags}

VIDEO OBJECTIVES:
1. Create platform-specific versions that maximize performance on each platform
2. Ensure accessibility and inclusive design across all versions
3. Optimize for discovery and algorithmic distribution
4. Maintain quality while meeting technical constraints
5. Create efficient workflow for multi-platform publishing

Focus on creating optimizations that:
- Meet each platform's specific technical requirements
- Maximize algorithmic reach and engagement
- Ensure accessibility for all users
- Maintain consistent branding across platforms
- Enable efficient content distribution workflow

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_video_prompt(self, task: Task, inputs: Dict[str, Any], 
                                        requirements: Dict[str, Any]) -> str:
        """Build prompt for general video tasks"""
        duration = requirements.get('duration', '5:00')
        format_type = requirements.get('format', 'mp4')
        resolution = requirements.get('resolution', '1080p')
        
        schema = {
            "video_concept": {
                "purpose": "string - what this video is intended to accomplish",
                "target_audience": "string - who will be watching",
                "viewing_context": "string - where/how this will be consumed",
                "key_messages": ["string - main points to communicate visually"]
            },
            "visual_approach": {
                "style": "string - overall visual style and aesthetic",
                "pacing": "string - editing rhythm and tempo",
                "visual_hierarchy": "string - how to organize visual elements",
                "brand_integration": "string - how to incorporate branding"
            },
            "technical_specifications": {
                "duration": "string - total video length",
                "resolution": "string - video resolution",
                "format": "string - output format",
                "quality_level": "string - production quality tier"
            }
        }
        
        return f"""Video Task: Create high-quality video content

USER REQUEST: {inputs.get('user_request', 'Create video')}
TASK: {task.task_name}

VIDEO REQUIREMENTS:
- Duration: {duration}
- Format: {format_type}
- Resolution: {resolution}

VIDEO OBJECTIVES:
1. Create professional video that serves its intended purpose
2. Ensure technical quality meets professional standards
3. Optimize for the specific use case and platform
4. Maintain consistency with overall content branding
5. Provide clear specifications for production

Focus on creating video that:
- Effectively serves its intended purpose
- Maintains professional quality throughout
- Works well in its intended context
- Meets all technical requirements
- Enhances the overall content experience

{self._build_json_schema_prompt(schema)}"""
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for video output validation"""
        return ['video_structure', 'short_clips_strategy', 'platform_specifications', 'video_concept']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate video output format"""
        # Check for main video structure
        video_fields = ['video_structure', 'short_clips_strategy', 'platform_specifications', 'video_concept']
        has_video_content = any(field in outputs for field in video_fields)
        
        if not has_video_content:
            return False
        
        # Validate that technical specifications exist
        spec_fields = ['technical_specifications', 'technical_requirements', 'quality_management']
        has_specifications = any(field in outputs for field in spec_fields)
        
        return has_specifications
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback video output"""
        user_request = inputs.get('user_request', 'video creation')
        duration = requirements.get('duration', '5:00')
        style = requirements.get('style', 'professional')
        
        return {
            'video_concept': {
                'purpose': f'Professional video for {user_request}',
                'target_audience': 'General audience',
                'viewing_context': 'Digital content consumption',
                'key_messages': [f'Main content related to {user_request}']
            },
            'visual_approach': {
                'style': style,
                'pacing': 'medium',
                'visual_hierarchy': 'clear and organized',
                'brand_integration': 'consistent branding throughout'
            },
            'technical_specifications': {
                'duration': duration,
                'resolution': '1080p',
                'format': 'MP4',
                'quality_level': 'high'
            },
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return video agent specializations"""
        return [
            "Professional video editing and compilation",
            "Short-form content creation (TikTok, Reels, Shorts)",
            "Multi-platform video optimization",
            "Motion graphics and visual effects",
            "Video accessibility and captions",
            "Algorithm optimization for social platforms",
            "Brand consistency in video content",
            "Technical video specifications and quality"
        ]
