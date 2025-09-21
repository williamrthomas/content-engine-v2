"""OpenRouter API client for LLM integration"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any
import aiohttp
from aiohttp import ClientSession, ClientTimeout

from ..core.config import settings
from .models import LLMRequest, LLMResponse, LLMUsage

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Async client for OpenRouter API"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openrouter_api_key
        self.session: Optional[ClientSession] = None
        self._model_pricing: Dict[str, Dict[str, float]] = {}
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_session(self):
        """Ensure HTTP session is created"""
        if self.session is None or self.session.closed:
            timeout = ClientTimeout(total=60, connect=10)
            self.session = ClientSession(
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/williamrthomas/content-engine-v2",
                    "X-Title": "Content Engine V2"
                }
            )
    
    async def close(self):
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_models(self) -> List[Dict[str, Any]]:
        """Get available models from OpenRouter"""
        await self._ensure_session()
        
        try:
            async with self.session.get(f"{self.BASE_URL}/models") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("data", [])
                    
                    # Cache pricing information
                    for model in models:
                        model_id = model.get("id")
                        pricing = model.get("pricing", {})
                        if model_id and pricing:
                            self._model_pricing[model_id] = {
                                "prompt": float(pricing.get("prompt", 0)),
                                "completion": float(pricing.get("completion", 0))
                            }
                    
                    logger.info(f"Retrieved {len(models)} models from OpenRouter")
                    return models
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get models: {response.status} - {error_text}")
                    return []
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return []
    
    async def chat_completion(self, request: LLMRequest) -> LLMResponse:
        """Send chat completion request to OpenRouter"""
        await self._ensure_session()
        
        start_time = time.time()
        
        # Prepare messages
        messages = []
        
        # Add system message if provided
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        
        # Add request messages
        messages.extend(request.messages)
        
        # Prepare request payload
        payload = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
        }
        
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens
        
        try:
            async with self.session.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    return self._parse_response(request, data, response_time)
                else:
                    error_text = await response.text()
                    logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                    raise Exception(f"OpenRouter API error: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    def _parse_response(self, request: LLMRequest, data: Dict[str, Any], response_time: float) -> LLMResponse:
        """Parse OpenRouter API response"""
        try:
            choice = data["choices"][0]
            message = choice["message"]
            usage_data = data.get("usage", {})
            
            # Calculate estimated cost
            model_pricing = self._model_pricing.get(request.model, {"prompt": 0, "completion": 0})
            prompt_cost = (usage_data.get("prompt_tokens", 0) / 1000) * model_pricing["prompt"]
            completion_cost = (usage_data.get("completion_tokens", 0) / 1000) * model_pricing["completion"]
            estimated_cost = prompt_cost + completion_cost
            
            usage = LLMUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
                estimated_cost=estimated_cost
            )
            
            return LLMResponse(
                id=request.id,
                model=data.get("model", request.model),
                content=message.get("content", ""),
                usage=usage,
                finish_reason=choice.get("finish_reason", "unknown"),
                response_time=response_time,
                metadata={
                    "raw_response": data,
                    "request_metadata": request.metadata
                }
            )
            
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error parsing OpenRouter response: {e}")
            logger.error(f"Response data: {data}")
            raise Exception(f"Failed to parse OpenRouter response: {e}")
    
    async def test_connection(self) -> bool:
        """Test connection to OpenRouter API"""
        try:
            models = await self.get_models()
            return len(models) > 0
        except Exception as e:
            logger.error(f"OpenRouter connection test failed: {e}")
            return False
