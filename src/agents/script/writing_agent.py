"""Writing agent for high-quality content creation"""

import json
from typing import Dict, Any, List
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory


class WritingAgent(StructuredLLMAgent):
    """High-quality writing agent for content creation with style and tone control"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Writing Agent",
            category=TaskCategory.SCRIPT,
            config=config
        )
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.SCRIPT:
            return False
        
        writing_keywords = [
            'write', 'create', 'draft', 'compose', 'generate',
            'script', 'content', 'article', 'blog', 'copy',
            'outline', 'introduction', 'conclusion', 'body'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in writing_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for writing tasks"""
        tone = requirements.get('tone', 'professional')
        style = requirements.get('style', 'informative')
        
        return f"""You are an expert content writer and copywriter with extensive experience in creating high-quality, engaging content across multiple formats and industries.

Your expertise includes:
- Professional writing with perfect grammar and style
- Audience-specific tone and voice adaptation
- SEO optimization and keyword integration
- Compelling storytelling and narrative structure
- Persuasive copywriting and call-to-action creation
- Technical and complex topic simplification
- Brand voice consistency and style guide adherence

Current writing parameters:
- Tone: {tone}
- Style: {style}
- Focus: Creating engaging, valuable content that serves the audience

You excel at:
1. Crafting compelling headlines and hooks
2. Structuring content for maximum readability
3. Integrating research and data naturally
4. Creating smooth transitions and flow
5. Writing persuasive calls-to-action
6. Adapting voice for different platforms and audiences
7. Optimizing content for both humans and search engines

Your writing is always original, well-researched, and tailored to the specific audience and purpose."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific writing task"""
        task_name_lower = task.task_name.lower()
        
        # Route to specific writing task handlers
        if 'outline' in task_name_lower:
            return await self._build_outline_prompt(task, inputs, requirements)
        elif any(word in task_name_lower for word in ['introduction', 'intro']):
            return await self._build_introduction_prompt(task, inputs, requirements)
        elif any(word in task_name_lower for word in ['conclusion', 'ending']):
            return await self._build_conclusion_prompt(task, inputs, requirements)
        elif any(word in task_name_lower for word in ['headline', 'title']):
            return await self._build_headline_prompt(task, inputs, requirements)
        elif 'script' in task_name_lower and 'full' in task_name_lower:
            return await self._build_full_script_prompt(task, inputs, requirements)
        else:
            return await self._build_general_content_prompt(task, inputs, requirements)
    
    async def _build_outline_prompt(self, task: Task, inputs: Dict[str, Any], 
                                  requirements: Dict[str, Any]) -> str:
        """Build prompt for content outline creation"""
        sections = requirements.get('sections', 5)
        include_intro = requirements.get('include_intro', True)
        include_conclusion = requirements.get('include_conclusion', True)
        
        schema = {
            "outline": {
                "title": "string - main title for the content",
                "introduction": {
                    "hook": "string - engaging opening hook",
                    "overview": "string - what the content will cover",
                    "value_proposition": "string - why reader should continue"
                } if include_intro else None,
                "main_sections": [
                    {
                        "section_number": "number - section order",
                        "title": "string - section title",
                        "key_points": ["string - main points to cover"],
                        "supporting_details": ["string - examples, stats, or details"],
                        "estimated_word_count": "number - words for this section"
                    }
                ],
                "conclusion": {
                    "summary_points": ["string - key takeaways"],
                    "call_to_action": "string - what reader should do next",
                    "closing_thought": "string - memorable ending"
                } if include_conclusion else None
            },
            "content_strategy": {
                "target_audience": "string - who this is written for",
                "primary_goal": "string - main objective of the content",
                "tone_guidelines": "string - how to maintain consistent tone",
                "seo_focus": "string - main keywords or topics to emphasize"
            },
            "estimated_metrics": {
                "total_word_count": "number - estimated total words",
                "reading_time": "string - estimated reading time",
                "complexity_level": "string - beginner/intermediate/advanced"
            }
        }
        
        return f"""Writing Task: Create a comprehensive content outline

USER REQUEST: {inputs.get('user_request', 'Create content')}
TASK: {task.task_name}

OUTLINE REQUIREMENTS:
- Number of main sections: {sections}
- Include introduction: {include_intro}
- Include conclusion: {include_conclusion}
- Target tone: {requirements.get('tone', 'professional')}

INSTRUCTIONS:
1. Create a logical, well-structured outline that flows naturally
2. Ensure each section builds upon the previous one
3. Include specific key points and supporting details for each section
4. Provide clear value proposition and engaging hooks
5. Estimate word counts for balanced content distribution
6. Consider SEO and audience engagement throughout

Focus on creating an outline that:
- Captures attention from the start
- Provides clear value to the target audience
- Maintains logical flow and progression
- Includes actionable insights and takeaways
- Ends with a strong call-to-action

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_full_script_prompt(self, task: Task, inputs: Dict[str, Any], 
                                      requirements: Dict[str, Any]) -> str:
        """Build prompt for full script writing (video/audio content)"""
        word_count = requirements.get('word_count', 1200)
        perspective_style = requirements.get('perspective_style', 'analytical')
        add_personal_insights = requirements.get('add_personal_insights', True)
        include_predictions = requirements.get('include_predictions', True)
        conversational_tone = requirements.get('conversational_tone', True)
        
        schema = {
            "script": {
                "title": "string - compelling title for the content",
                "hook": "string - attention-grabbing opening (first 15 seconds)",
                "introduction": "string - introduce topic and value proposition",
                "main_content": [
                    {
                        "section_title": "string - section heading",
                        "content": "string - full written content for this section",
                        "key_points": ["string - main takeaways"],
                        "transitions": "string - how to transition to next section",
                        "timestamp_estimate": "string - estimated time for this section"
                    }
                ],
                "expert_analysis": {
                    "perspective": "string - your analytical perspective on the topic",
                    "insights": ["string - unique insights and observations"],
                    "predictions": ["string - future predictions or trends"] if include_predictions else None,
                    "personal_take": "string - your personal viewpoint" if add_personal_insights else None
                },
                "conclusion": "string - strong closing that reinforces key messages",
                "call_to_action": "string - what you want viewers to do next"
            },
            "script_metadata": {
                "estimated_duration": "string - estimated speaking time",
                "word_count": "number - actual word count",
                "tone": "string - overall tone used",
                "target_audience": "string - who this is for",
                "key_messages": ["string - main messages to communicate"]
            },
            "production_notes": {
                "emphasis_points": ["string - where to add vocal emphasis"],
                "pause_suggestions": ["string - where to pause for effect"],
                "visual_cues": ["string - suggestions for visual elements"]
            }
        }
        
        return f"""Writing Task: Create a full script with expert perspective and analysis

USER REQUEST: {inputs.get('user_request', 'Create script content')}
TASK: {task.task_name}

SCRIPT REQUIREMENTS:
- Target word count: {word_count}
- Perspective style: {perspective_style}
- Add personal insights: {add_personal_insights}
- Include predictions: {include_predictions}
- Conversational tone: {conversational_tone}
- Tone: {requirements.get('tone', 'professional')}

INSTRUCTIONS:
1. Write a complete, engaging script ready for recording
2. Include a strong hook that captures attention immediately
3. Provide expert analysis and unique perspective throughout
4. Use conversational language that sounds natural when spoken
5. Include smooth transitions between sections
6. Add personal insights and predictions where relevant
7. End with a compelling call-to-action

Focus on creating content that:
- Sounds natural and engaging when spoken aloud
- Provides genuine value and expert insights
- Maintains audience attention throughout
- Includes your unique perspective and analysis
- Flows logically from point to point
- Ends with clear next steps for the audience

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_headline_prompt(self, task: Task, inputs: Dict[str, Any], 
                                   requirements: Dict[str, Any]) -> str:
        """Build prompt for headline generation"""
        variations = requirements.get('variations', 3)
        seo_optimized = requirements.get('seo_optimized', True)
        char_limit = requirements.get('char_limit', 60)
        
        schema = {
            "headlines": [
                {
                    "headline": "string - the headline text",
                    "character_count": "number - length in characters",
                    "style": "string - style used (curiosity, benefit, how-to, etc.)",
                    "seo_score": "number - 1-10 SEO optimization score",
                    "engagement_potential": "number - 1-10 click potential"
                }
            ],
            "meta_descriptions": [
                {
                    "description": "string - meta description text",
                    "character_count": "number - length in characters",
                    "includes_keywords": "boolean - contains target keywords",
                    "call_to_action": "string - CTA included in description"
                }
            ],
            "analysis": {
                "target_keywords": ["string - main keywords used"],
                "headline_strategy": "string - approach used for headlines",
                "audience_appeal": "string - why these will appeal to target audience"
            }
        }
        
        return f"""Writing Task: Create compelling, SEO-optimized headlines

USER REQUEST: {inputs.get('user_request', 'Create headlines')}
TASK: {task.task_name}

HEADLINE REQUIREMENTS:
- Number of variations: {variations}
- SEO optimized: {seo_optimized}
- Character limit: {char_limit}
- Target tone: {requirements.get('tone', 'professional')}

INSTRUCTIONS:
1. Create multiple headline variations using different approaches
2. Optimize for both search engines and human appeal
3. Stay within character limits for platform compatibility
4. Include power words and emotional triggers
5. Create corresponding meta descriptions
6. Ensure headlines accurately represent the content

Headline styles to consider:
- How-to headlines (practical value)
- Number-based headlines (specific benefit)
- Question headlines (curiosity-driven)
- Benefit-focused headlines (clear value)
- Urgency headlines (time-sensitive)
- Curiosity headlines (intrigue-based)

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_content_prompt(self, task: Task, inputs: Dict[str, Any], 
                                          requirements: Dict[str, Any]) -> str:
        """Build prompt for general content writing"""
        target_words = requirements.get('target_words', requirements.get('word_count', 500))
        include_examples = requirements.get('include_examples', True)
        add_statistics = requirements.get('add_statistics', True)
        include_cta = requirements.get('include_cta', False)
        
        schema = {
            "content": {
                "title": "string - content title",
                "body": "string - main content body",
                "key_points": ["string - main takeaways"],
                "examples": ["string - relevant examples"] if include_examples else None,
                "statistics": ["string - supporting statistics"] if add_statistics else None,
                "call_to_action": "string - compelling CTA" if include_cta else None
            },
            "content_metrics": {
                "word_count": "number - actual word count",
                "readability_score": "number - 1-10 readability",
                "tone_consistency": "number - 1-10 tone consistency",
                "value_score": "number - 1-10 value provided to reader"
            },
            "seo_elements": {
                "primary_keywords": ["string - main keywords used"],
                "secondary_keywords": ["string - supporting keywords"],
                "keyword_density": "number - percentage of keyword usage",
                "meta_suggestions": "string - suggested meta description"
            }
        }
        
        return f"""Writing Task: Create high-quality content

USER REQUEST: {inputs.get('user_request', 'Create content')}
TASK: {task.task_name}

CONTENT REQUIREMENTS:
- Target word count: {target_words}
- Include examples: {include_examples}
- Add statistics: {add_statistics}
- Include call-to-action: {include_cta}
- Tone: {requirements.get('tone', 'professional')}

INSTRUCTIONS:
1. Write engaging, valuable content that serves the audience
2. Maintain consistent tone and voice throughout
3. Include relevant examples and statistics where appropriate
4. Structure content for easy reading and comprehension
5. Optimize for search engines while prioritizing readability
6. End with appropriate call-to-action if required

Focus on creating content that:
- Provides genuine value to the reader
- Is well-structured and easy to follow
- Includes actionable insights and takeaways
- Maintains reader engagement throughout
- Achieves the specified word count naturally
- Incorporates relevant keywords organically

{self._build_json_schema_prompt(schema)}"""
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for writing output validation"""
        return ['content']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate writing output format"""
        # Check if main content exists
        if 'content' not in outputs and 'script' not in outputs and 'outline' not in outputs and 'headlines' not in outputs:
            return False
        
        # Validate content length
        content_fields = ['content', 'script', 'outline', 'headlines']
        has_substantial_content = False
        
        for field in content_fields:
            if field in outputs:
                content = outputs[field]
                if isinstance(content, str) and len(content) > 50:
                    has_substantial_content = True
                elif isinstance(content, dict) and len(str(content)) > 50:
                    has_substantial_content = True
                elif isinstance(content, list) and len(content) > 0:
                    has_substantial_content = True
        
        return has_substantial_content
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback writing output"""
        user_request = inputs.get('user_request', 'content creation')
        target_words = requirements.get('target_words', requirements.get('word_count', 500))
        
        return {
            'content': {
                'title': f"Content for {user_request}",
                'body': f"This is fallback content generated for the task '{task.task_name}'. The requested content about '{user_request}' would normally be created with approximately {target_words} words of high-quality, engaging material. This fallback was generated because the LLM service was unavailable.",
                'key_points': [
                    f"Main point about {user_request}",
                    "Supporting information and details",
                    "Actionable insights and takeaways"
                ]
            },
            'content_metrics': {
                'word_count': len(f"Fallback content for {user_request}"),
                'readability_score': 7,
                'tone_consistency': 6,
                'value_score': 5
            },
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return writing agent specializations"""
        return [
            "Blog post and article writing",
            "Script writing for video/audio",
            "Content outline creation",
            "Headline and title generation",
            "SEO-optimized copywriting",
            "Technical content simplification",
            "Brand voice adaptation",
            "Call-to-action creation"
        ]
