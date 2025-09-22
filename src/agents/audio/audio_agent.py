"""Audio agent for high-quality audio generation and processing"""

import json
from typing import Dict, Any, List
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory


class AudioAgent(StructuredLLMAgent):
    """High-quality audio agent for narration, music, and audio processing"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Audio Agent",
            category=TaskCategory.AUDIO,
            config=config
        )
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.AUDIO:
            return False
        
        audio_keywords = [
            'audio', 'narration', 'voice', 'speech', 'music', 'sound',
            'record', 'tts', 'background', 'effects', 'mixing'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in audio_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for audio tasks"""
        return """You are an expert audio producer and sound engineer with extensive experience in:

- Professional voice-over and narration production
- Audio post-production and mixing techniques
- Music selection and audio branding
- Podcast and video audio optimization
- Text-to-speech optimization and voice selection
- Audio accessibility and clarity standards
- Platform-specific audio requirements

Your expertise includes:
1. Creating engaging, professional narration scripts and direction
2. Selecting appropriate voice styles and characteristics for content
3. Designing audio experiences that enhance content engagement
4. Optimizing audio for different platforms and use cases
5. Balancing narration, music, and sound effects effectively
6. Ensuring audio accessibility and clarity standards
7. Managing audio technical specifications and quality

You excel at:
- Crafting narration that sounds natural and engaging when spoken
- Selecting voice characteristics that match content and audience
- Creating audio experiences that enhance rather than distract
- Optimizing audio for both quality and file size
- Ensuring consistent audio branding across content
- Meeting platform-specific audio requirements and standards

Your audio productions are always professional, engaging, and optimized for their intended use."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific audio task"""
        task_name_lower = task.task_name.lower()
        
        # Route to specific audio task handlers
        if 'narration' in task_name_lower or 'record' in task_name_lower:
            return await self._build_narration_prompt(task, inputs, requirements)
        elif 'music' in task_name_lower or 'background' in task_name_lower:
            return await self._build_background_music_prompt(task, inputs, requirements)
        else:
            return await self._build_general_audio_prompt(task, inputs, requirements)
    
    async def _build_narration_prompt(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> str:
        """Build prompt for narration and voice-over tasks"""
        voice_style = requirements.get('voice_style', 'professional')
        pace = requirements.get('pace', 'medium')
        emphasis_on_numbers = requirements.get('emphasis_on_numbers', True)
        clear_pronunciation = requirements.get('clear_pronunciation', True)
        
        schema = {
            "narration_specification": {
                "voice_characteristics": {
                    "voice_type": "string - recommended voice type (male/female/neutral)",
                    "age_range": "string - apparent age of voice (young adult/middle-aged/mature)",
                    "accent": "string - accent or regional characteristics",
                    "tone_quality": "string - voice tone (warm/authoritative/friendly/energetic)",
                    "speaking_style": "string - delivery style (conversational/professional/enthusiastic)"
                },
                "delivery_specifications": {
                    "speaking_pace": "string - speed of delivery (slow/medium/fast)",
                    "emphasis_points": ["string - words or phrases to emphasize"],
                    "pause_locations": ["string - where to add dramatic pauses"],
                    "inflection_notes": ["string - how to vary tone and pitch"],
                    "pronunciation_guide": ["string - specific pronunciation instructions"]
                },
                "technical_requirements": {
                    "audio_quality": "string - recording quality specifications",
                    "file_format": "string - output format (MP3/WAV/AAC)",
                    "bit_rate": "string - audio bit rate for quality",
                    "sample_rate": "string - audio sample rate",
                    "mono_stereo": "string - channel configuration"
                }
            },
            "script_optimization": {
                "readability_score": "number - 1-10 how easy to read aloud",
                "estimated_duration": "string - expected speaking time",
                "breath_marks": ["string - suggested breathing points"],
                "difficult_words": ["string - words that need special attention"],
                "flow_improvements": ["string - suggestions for better spoken flow"]
            },
            "engagement_strategy": {
                "hook_delivery": "string - how to deliver opening hook",
                "energy_maintenance": "string - keeping listener engaged throughout",
                "call_to_action_emphasis": "string - how to deliver CTA effectively",
                "emotional_connection": "string - creating connection with audience"
            },
            "production_notes": {
                "background_music": "string - whether and what type of music to add",
                "sound_effects": ["string - any sound effects to include"],
                "noise_reduction": "string - background noise considerations",
                "post_processing": ["string - audio effects and processing needed"]
            }
        }
        
        return f"""Audio Task: Create professional narration specification

USER REQUEST: {inputs.get('user_request', 'Create narration')}
TASK: {task.task_name}

NARRATION REQUIREMENTS:
- Voice style: {voice_style}
- Speaking pace: {pace}
- Emphasize numbers: {emphasis_on_numbers}
- Clear pronunciation: {clear_pronunciation}

AUDIO OBJECTIVES:
1. Create engaging narration that holds listener attention
2. Ensure clarity and professional delivery quality
3. Match voice characteristics to content and audience
4. Optimize for the intended platform and use case
5. Provide detailed technical specifications for production

Focus on creating narration that:
- Sounds natural and conversational when spoken aloud
- Maintains consistent energy and engagement throughout
- Clearly communicates key information and messages
- Appeals to the target audience demographic
- Meets professional audio production standards

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_background_music_prompt(self, task: Task, inputs: Dict[str, Any], 
                                           requirements: Dict[str, Any]) -> str:
        """Build prompt for background music and audio atmosphere"""
        music_style = requirements.get('music_style', 'tech/upbeat')
        volume_level = requirements.get('volume_level', 'subtle')
        intro_outro_emphasis = requirements.get('intro_outro_emphasis', True)
        transition_sounds = requirements.get('transition_sounds', True)
        
        schema = {
            "music_selection": {
                "primary_track": {
                    "genre": "string - music genre/style",
                    "mood": "string - emotional mood of the music",
                    "tempo": "string - beats per minute or pace description",
                    "instrumentation": "string - types of instruments/sounds",
                    "energy_level": "string - high/medium/low energy"
                },
                "track_structure": {
                    "intro_music": "string - opening music characteristics",
                    "main_background": "string - music during main content",
                    "transition_stings": ["string - music for section transitions"],
                    "outro_music": "string - closing music characteristics",
                    "duration_breakdown": "string - timing for each section"
                }
            },
            "audio_mixing": {
                "volume_levels": {
                    "music_volume": "string - background music level",
                    "narration_volume": "string - voice level relative to music",
                    "effects_volume": "string - sound effects level",
                    "dynamic_range": "string - how volume changes throughout"
                },
                "eq_settings": {
                    "music_eq": "string - frequency adjustments for music",
                    "voice_eq": "string - frequency adjustments for narration",
                    "overall_balance": "string - how all elements work together"
                }
            },
            "sound_design": {
                "ambient_sounds": ["string - background atmosphere sounds"],
                "transition_effects": ["string - sounds for section changes"],
                "emphasis_sounds": ["string - sounds to highlight key points"],
                "branding_audio": "string - consistent audio branding elements"
            },
            "technical_specifications": {
                "file_formats": ["string - required audio formats"],
                "quality_settings": "string - bit rate and sample rate",
                "stereo_imaging": "string - how to use stereo field",
                "compression": "string - dynamic range compression settings",
                "mastering_notes": "string - final mastering considerations"
            }
        }
        
        return f"""Audio Task: Create background music and audio atmosphere

USER REQUEST: {inputs.get('user_request', 'Create background audio')}
TASK: {task.task_name}

BACKGROUND AUDIO REQUIREMENTS:
- Music style: {music_style}
- Volume level: {volume_level}
- Intro/outro emphasis: {intro_outro_emphasis}
- Transition sounds: {transition_sounds}

AUDIO OBJECTIVES:
1. Create audio atmosphere that enhances content without distraction
2. Maintain consistent mood and energy throughout the piece
3. Provide clear audio branding and professional polish
4. Balance all audio elements for optimal listening experience
5. Meet technical requirements for intended platform

Focus on creating audio that:
- Supports and enhances the main content
- Maintains professional quality and consistency
- Creates the right emotional atmosphere
- Works well across different playback systems
- Follows platform-specific audio guidelines

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_audio_prompt(self, task: Task, inputs: Dict[str, Any], 
                                        requirements: Dict[str, Any]) -> str:
        """Build prompt for general audio tasks"""
        duration = requirements.get('duration', '2:30')
        format_type = requirements.get('format', 'mp3')
        
        schema = {
            "audio_concept": {
                "purpose": "string - what this audio is intended to accomplish",
                "target_audience": "string - who will be listening",
                "listening_context": "string - where/how this will be consumed",
                "key_messages": ["string - main points to communicate through audio"]
            },
            "audio_elements": {
                "primary_content": "string - main audio content (voice/music/effects)",
                "supporting_elements": ["string - additional audio components"],
                "audio_hierarchy": "string - how different elements are prioritized",
                "timing_structure": "string - how audio unfolds over time"
            },
            "production_specifications": {
                "duration": "string - total length of audio",
                "file_format": "string - output format",
                "quality_level": "string - production quality tier",
                "delivery_requirements": "string - how audio will be delivered/used"
            }
        }
        
        return f"""Audio Task: Create high-quality audio content

USER REQUEST: {inputs.get('user_request', 'Create audio')}
TASK: {task.task_name}

AUDIO REQUIREMENTS:
- Duration: {duration}
- Format: {format_type}

AUDIO OBJECTIVES:
1. Create professional audio that serves its intended purpose
2. Ensure technical quality meets professional standards
3. Optimize for the specific use case and platform
4. Maintain consistency with overall content branding
5. Provide clear specifications for production

Focus on creating audio that:
- Effectively serves its intended purpose
- Maintains professional quality throughout
- Works well in its intended context
- Meets all technical requirements
- Enhances the overall content experience

{self._build_json_schema_prompt(schema)}"""
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for audio output validation"""
        return ['narration_specification', 'music_selection', 'audio_concept']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate audio output format"""
        # Check for main audio structure
        audio_fields = ['narration_specification', 'music_selection', 'audio_concept']
        has_audio_content = any(field in outputs for field in audio_fields)
        
        if not has_audio_content:
            return False
        
        # Validate that technical specifications exist
        spec_fields = ['technical_requirements', 'technical_specifications', 'production_specifications']
        has_specifications = any(field in outputs for field in spec_fields)
        
        return has_specifications
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback audio output"""
        user_request = inputs.get('user_request', 'audio creation')
        duration = requirements.get('duration', '2:30')
        voice_style = requirements.get('voice_style', 'professional')
        
        return {
            'audio_concept': {
                'purpose': f'Professional audio for {user_request}',
                'target_audience': 'General audience',
                'listening_context': 'Digital content consumption',
                'key_messages': [f'Main content related to {user_request}']
            },
            'narration_specification': {
                'voice_characteristics': {
                    'voice_type': 'neutral',
                    'tone_quality': voice_style,
                    'speaking_style': 'conversational'
                },
                'delivery_specifications': {
                    'speaking_pace': 'medium',
                    'emphasis_points': ['key terms', 'important numbers'],
                    'pause_locations': ['after main points', 'before conclusions']
                }
            },
            'production_specifications': {
                'duration': duration,
                'file_format': 'MP3',
                'quality_level': 'high',
                'delivery_requirements': f'Optimized for {task.task_name}'
            },
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return audio agent specializations"""
        return [
            "Professional narration and voice-over",
            "Background music selection and mixing",
            "Podcast audio production",
            "Video audio optimization", 
            "Text-to-speech optimization",
            "Audio branding and consistency",
            "Platform-specific audio requirements",
            "Audio accessibility and clarity"
        ]
