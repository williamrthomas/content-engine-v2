"""Research agent for gathering and analyzing information"""

import json
from typing import Dict, Any, List
from ..llm_agent import StructuredLLMAgent
from ...core.models import Task, TaskCategory


class ResearchAgent(StructuredLLMAgent):
    """High-quality research agent for information gathering and analysis"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(
            name="Research Agent",
            category=TaskCategory.SCRIPT,
            config=config
        )
    
    async def validate_task(self, task: Task) -> bool:
        """Validate if this agent can handle the task"""
        if task.category != TaskCategory.SCRIPT:
            return False
        
        research_keywords = [
            'research', 'source', 'analyze', 'investigate', 'gather',
            'collect', 'find', 'discover', 'explore', 'study'
        ]
        
        return any(keyword in task.task_name.lower() for keyword in research_keywords)
    
    async def _build_system_prompt(self, task: Task, inputs: Dict[str, Any], 
                                 requirements: Dict[str, Any]) -> str:
        """Build system prompt for research tasks"""
        return """You are an expert research analyst specializing in comprehensive information gathering and trend analysis. Your expertise includes:

- Social media trend analysis and content curation
- Data-driven research with credible source identification
- Market intelligence and competitive analysis
- Content strategy and audience insights
- Statistical analysis and pattern recognition

You excel at:
1. Identifying high-quality, credible sources
2. Analyzing trends and extracting key insights
3. Synthesizing complex information into actionable findings
4. Providing context and background for trending topics
5. Fact-checking and verification of information

Your research is thorough, unbiased, and focused on providing maximum value for content creation."""
    
    async def _build_user_prompt(self, task: Task, inputs: Dict[str, Any], 
                               requirements: Dict[str, Any]) -> str:
        """Build user prompt for specific research task"""
        user_request = inputs.get('user_request', 'No specific request provided')
        
        # Handle X post sourcing specifically
        if 'source_x_posts' in task.task_name.lower() or 'twitter' in task.task_name.lower():
            return await self._build_x_sourcing_prompt(task, inputs, requirements)
        
        # Handle general research tasks
        return await self._build_general_research_prompt(task, inputs, requirements)
    
    async def _build_x_sourcing_prompt(self, task: Task, inputs: Dict[str, Any], 
                                     requirements: Dict[str, Any]) -> str:
        """Build prompt for X (Twitter) post sourcing and analysis"""
        topics = requirements.get('topics', ['AI', 'technology'])
        post_count = requirements.get('post_count', 15)
        time_frame = requirements.get('time_frame', '24 hours')
        min_engagement = requirements.get('min_engagement', 100)
        
        schema = {
            "trending_topics": [
                {
                    "topic": "string - main topic/theme",
                    "posts": [
                        {
                            "content": "string - post content/summary",
                            "author": "string - author handle or name",
                            "engagement_score": "number - estimated engagement",
                            "relevance_score": "number - 1-10 relevance to topic",
                            "novelty_score": "number - 1-10 how new/unique",
                            "controversy_score": "number - 1-10 how controversial",
                            "key_insights": ["string - key takeaways"],
                            "context": "string - background context needed"
                        }
                    ]
                }
            ],
            "analysis_summary": {
                "total_posts_analyzed": "number",
                "top_themes": ["string - main themes identified"],
                "trending_keywords": ["string - most mentioned keywords"],
                "sentiment_overview": "string - overall sentiment",
                "recommendation": "string - which posts/topics to prioritize"
            },
            "quality_metrics": {
                "source_credibility": "number - 1-10 average credibility",
                "content_freshness": "number - 1-10 how recent/fresh",
                "engagement_potential": "number - 1-10 viral potential"
            }
        }
        
        return f"""Research Task: Analyze and curate trending X (Twitter) posts for content creation

USER REQUEST: {inputs.get('user_request', 'Create trending content')}

RESEARCH PARAMETERS:
- Topics to focus on: {', '.join(topics)}
- Target post count: {post_count}
- Time frame: {time_frame}
- Minimum engagement threshold: {min_engagement}
- Prioritize verified accounts: {requirements.get('verified_accounts_priority', True)}

INSTRUCTIONS:
1. Identify the most engaging and relevant posts from the specified topics
2. Analyze trends, patterns, and emerging themes
3. Evaluate each post for relevance, novelty, and engagement potential
4. Provide context and background information for each selected post
5. Rank and prioritize content based on viral potential and audience value

Focus on posts that are:
- Highly engaging (likes, retweets, comments)
- From credible sources or verified accounts
- Contain unique insights or breaking news
- Spark meaningful discussion or debate
- Relevant to current events and trends

{self._build_json_schema_prompt(schema)}"""
    
    async def _build_general_research_prompt(self, task: Task, inputs: Dict[str, Any], 
                                           requirements: Dict[str, Any]) -> str:
        """Build prompt for general research tasks"""
        min_sources = requirements.get('min_sources', 3)
        include_competitors = requirements.get('include_competitors', False)
        target_keywords = requirements.get('target_keywords', False)
        
        schema = {
            "research_summary": "string - comprehensive overview of findings",
            "key_findings": [
                {
                    "finding": "string - main insight or discovery",
                    "evidence": "string - supporting data or examples",
                    "source": "string - credible source URL or citation",
                    "relevance_score": "number - 1-10 relevance to topic"
                }
            ],
            "sources": [
                {
                    "url": "string - source URL",
                    "title": "string - source title",
                    "credibility_score": "number - 1-10 source credibility",
                    "key_points": ["string - main points from this source"]
                }
            ],
            "statistics": [
                {
                    "statistic": "string - relevant statistic or data point",
                    "source": "string - where this data comes from",
                    "context": "string - why this matters"
                }
            ],
            "trends_analysis": {
                "current_trends": ["string - current trends in the topic"],
                "emerging_patterns": ["string - new patterns or developments"],
                "market_insights": "string - market or industry insights"
            },
            "content_opportunities": [
                "string - opportunities for content creation based on research"
            ]
        }
        
        return f"""Research Task: Comprehensive analysis and information gathering

USER REQUEST: {inputs.get('user_request', 'Research this topic')}
TASK: {task.task_name}

RESEARCH REQUIREMENTS:
- Minimum credible sources: {min_sources}
- Include competitor analysis: {include_competitors}
- Target keyword research: {target_keywords}

INSTRUCTIONS:
1. Conduct thorough research on the specified topic
2. Identify and verify credible sources and statistics
3. Analyze current trends and emerging patterns
4. Extract key insights and actionable findings
5. Provide context and background information
6. Identify content creation opportunities

Focus on:
- Recent, credible, and authoritative sources
- Data-driven insights and statistics
- Expert opinions and case studies
- Current market trends and developments
- Actionable insights for content creation

{self._build_json_schema_prompt(schema)}"""
    
    async def _get_required_output_fields(self) -> List[str]:
        """Required fields for research output validation"""
        return ['research_summary', 'key_findings', 'sources']
    
    async def _validate_output_format(self, outputs: Dict[str, Any]) -> bool:
        """Validate research output format"""
        required_fields = await self._get_required_output_fields()
        
        # Check required fields exist
        for field in required_fields:
            if field not in outputs:
                return False
        
        # Validate key_findings structure
        if 'key_findings' in outputs:
            findings = outputs['key_findings']
            if not isinstance(findings, list) or len(findings) == 0:
                return False
        
        # Validate sources structure  
        if 'sources' in outputs:
            sources = outputs['sources']
            if not isinstance(sources, list) or len(sources) == 0:
                return False
        
        return True
    
    async def _create_fallback_output(self, task: Task, inputs: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback research output"""
        user_request = inputs.get('user_request', 'research topic')
        
        return {
            'research_summary': f"Research analysis for: {user_request}. This is fallback content generated when LLM service was unavailable.",
            'key_findings': [
                {
                    'finding': f"Primary insight about {user_request}",
                    'evidence': "Supporting evidence would be gathered from credible sources",
                    'source': "https://example.com/fallback-source",
                    'relevance_score': 8
                }
            ],
            'sources': [
                {
                    'url': 'https://example.com/source1',
                    'title': f'Credible source about {user_request}',
                    'credibility_score': 8,
                    'key_points': ['Key point 1', 'Key point 2']
                }
            ],
            'status': 'fallback_generated',
            'fallback_reason': 'LLM service unavailable'
        }
    
    async def _get_specializations(self) -> List[str]:
        """Return research agent specializations"""
        return [
            "Social media trend analysis",
            "X (Twitter) post curation",
            "Market research and analysis", 
            "Competitive intelligence",
            "Statistical data gathering",
            "Source credibility verification",
            "Content opportunity identification"
        ]
