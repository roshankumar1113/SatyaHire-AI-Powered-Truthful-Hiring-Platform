"""
AI Client - Unified interface for multiple AI providers with automatic fallback
"""

from typing import Optional, Dict, Any, List
import logging
from enum import Enum

from app.utils.api_key_manager import MultiProviderKeyManager, AIProvider
from app.config import get_settings

logger = logging.getLogger(__name__)


class AIClientError(Exception):
    """Base exception for AI client errors"""
    pass


class AIClient:
    """
    Unified AI client with multi-provider support and automatic fallback.
    
    Features:
    - Multiple API key support per provider
    - Automatic key rotation
    - Provider fallback (OpenAI -> Gemini -> Anthropic)
    - Retry logic with different keys
    - Thread-safe operations
    """
    
    def __init__(self):
        """Initialize AI client with key manager"""
        self.settings = get_settings()
        self.key_manager = MultiProviderKeyManager()
        
        # Load API keys from settings
        self._load_api_keys()
        
        # Default configuration
        self.default_provider = AIProvider(self.settings.DEFAULT_AI_PROVIDER)
        self.model = self.settings.AI_MODEL
        self.temperature = self.settings.AI_TEMPERATURE
        self.max_tokens = self.settings.AI_MAX_TOKENS
    
    def _load_api_keys(self):
        """Load API keys from settings"""
        # OpenAI
        openai_keys = self.settings.get_openai_keys()
        if openai_keys:
            self.key_manager.add_provider(AIProvider.OPENAI, openai_keys)
            logger.info(f"Loaded {len(openai_keys)} OpenAI API keys")
        
        # Gemini
        gemini_keys = self.settings.get_gemini_keys()
        if gemini_keys:
            self.key_manager.add_provider(AIProvider.GEMINI, gemini_keys)
            logger.info(f"Loaded {len(gemini_keys)} Gemini API keys")
        
        # Anthropic
        anthropic_keys = self.settings.get_anthropic_keys()
        if anthropic_keys:
            self.key_manager.add_provider(AIProvider.ANTHROPIC, anthropic_keys)
            logger.info(f"Loaded {len(anthropic_keys)} Anthropic API keys")
        
        if not self.key_manager.get_available_providers():
            logger.warning("No AI API keys configured!")
    
    def generate_text(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text using AI with automatic fallback.
        
        Args:
            prompt: Input prompt
            provider: Preferred AI provider (optional)
            model: Model name (optional)
            temperature: Temperature setting (optional)
            max_tokens: Max tokens (optional)
            
        Returns:
            str: Generated text
            
        Raises:
            AIClientError: If all providers and keys fail
        """
        provider = provider or self.default_provider
        model = model or self.model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        # Try with fallback
        api_key, used_provider = self.key_manager.get_key_with_fallback(provider)
        
        if not api_key:
            raise AIClientError("No API keys available for any provider")
        
        # Try all keys for the provider
        all_keys = self.key_manager.get_all_keys_for_provider(used_provider)
        
        for key in all_keys:
            try:
                if used_provider == AIProvider.OPENAI:
                    return self._call_openai(key, prompt, model, temperature, max_tokens)
                elif used_provider == AIProvider.GEMINI:
                    return self._call_gemini(key, prompt, model, temperature, max_tokens)
                elif used_provider == AIProvider.ANTHROPIC:
                    return self._call_anthropic(key, prompt, model, temperature, max_tokens)
            except Exception as e:
                logger.warning(f"Failed with {used_provider} key: {str(e)}")
                continue
        
        raise AIClientError(f"All API keys failed for {used_provider}")
    
    def _call_openai(
        self,
        api_key: str,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """
        Call OpenAI API
        
        Args:
            api_key: OpenAI API key
            prompt: Input prompt
            model: Model name
            temperature: Temperature
            max_tokens: Max tokens
            
        Returns:
            str: Generated text
        """
        try:
            # Import here to avoid dependency issues
            import openai
            
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _call_gemini(
        self,
        api_key: str,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """
        Call Gemini API
        
        Args:
            api_key: Gemini API key
            prompt: Input prompt
            model: Model name
            temperature: Temperature
            max_tokens: Max tokens
            
        Returns:
            str: Generated text
        """
        try:
            # Import here to avoid dependency issues
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            model_instance = genai.GenerativeModel(model or 'gemini-pro')
            
            response = model_instance.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
            )
            
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def _call_anthropic(
        self,
        api_key: str,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """
        Call Anthropic API
        
        Args:
            api_key: Anthropic API key
            prompt: Input prompt
            model: Model name
            temperature: Temperature
            max_tokens: Max tokens
            
        Returns:
            str: Generated text
        """
        try:
            # Import here to avoid dependency issues
            import anthropic
            
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model=model or "claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
    
    def generate_interview_question(
        self,
        job_description: str,
        candidate_background: str,
        question_number: int,
    ) -> str:
        """
        Generate interview question based on job description and candidate background.
        
        Args:
            job_description: Job description
            candidate_background: Candidate's background
            question_number: Question number (1-5)
            
        Returns:
            str: Generated interview question
        """
        prompt = f"""
        You are an AI interviewer. Generate a relevant interview question.
        
        Job Description: {job_description}
        Candidate Background: {candidate_background}
        Question Number: {question_number}
        
        Generate a thoughtful, relevant interview question that:
        1. Relates to the job requirements
        2. Assesses the candidate's skills and experience
        3. Is clear and professional
        4. Encourages detailed responses
        
        Return only the question, nothing else.
        """
        
        return self.generate_text(prompt, max_tokens=200)
    
    def analyze_interview_answer(
        self,
        question: str,
        answer: str,
        job_requirements: str,
    ) -> Dict[str, Any]:
        """
        Analyze candidate's interview answer.
        
        Args:
            question: Interview question
            answer: Candidate's answer
            job_requirements: Job requirements
            
        Returns:
            Dict: Analysis results with score and feedback
        """
        prompt = f"""
        Analyze this interview answer and provide a score and feedback.
        
        Question: {question}
        Answer: {answer}
        Job Requirements: {job_requirements}
        
        Provide analysis in this format:
        Score: [0-10]
        Strengths: [bullet points]
        Areas for Improvement: [bullet points]
        Overall Assessment: [brief summary]
        """
        
        analysis = self.generate_text(prompt, max_tokens=500)
        
        # Parse the response (simplified)
        return {
            "raw_analysis": analysis,
            "question": question,
            "answer": answer,
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get AI client status
        
        Returns:
            Dict: Status information
        """
        return {
            "available_providers": [p.value for p in self.key_manager.get_available_providers()],
            "default_provider": self.default_provider.value,
            "model": self.model,
            "key_manager": str(self.key_manager),
        }


# Singleton instance
_ai_client: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """
    Get singleton AI client instance
    
    Returns:
        AIClient: AI client instance
    """
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient()
    return _ai_client
