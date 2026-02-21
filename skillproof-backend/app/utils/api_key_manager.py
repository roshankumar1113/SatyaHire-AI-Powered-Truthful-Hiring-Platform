"""
API Key Manager - Thread-safe key rotation and fallback
"""

import threading
from typing import List, Optional
from enum import Enum


class AIProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"


class APIKeyManager:
    """
    Thread-safe API key manager with round-robin rotation and automatic fallback.
    
    Features:
    - Round-robin key rotation
    - Automatic fallback to next key on failure
    - Thread-safe implementation
    - No key logging for security
    """
    
    def __init__(self, keys: List[str], provider: AIProvider):
        """
        Initialize API Key Manager
        
        Args:
            keys: List of API keys
            provider: AI provider name
        """
        if not keys:
            raise ValueError(f"No API keys provided for {provider}")
        
        self.keys = keys
        self.provider = provider
        self.current_index = 0
        self.lock = threading.Lock()
        self.failed_keys = set()  # Track temporarily failed keys
    
    def get_next_key(self) -> str:
        """
        Get next API key using round-robin rotation.
        Thread-safe implementation.
        
        Returns:
            str: Next API key in rotation
        """
        with self.lock:
            key = self.keys[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.keys)
            return key
    
    def get_all_keys(self) -> List[str]:
        """
        Get all available keys (excluding temporarily failed ones)
        
        Returns:
            List[str]: List of available API keys
        """
        return [key for key in self.keys if key not in self.failed_keys]
    
    def mark_key_failed(self, key: str):
        """
        Mark a key as temporarily failed
        
        Args:
            key: The failed API key
        """
        with self.lock:
            self.failed_keys.add(key)
    
    def reset_failed_keys(self):
        """Reset all failed keys (call periodically or after cooldown)"""
        with self.lock:
            self.failed_keys.clear()
    
    def get_key_count(self) -> int:
        """Get total number of keys"""
        return len(self.keys)
    
    def get_available_key_count(self) -> int:
        """Get number of available (non-failed) keys"""
        return len(self.get_all_keys())
    
    def __repr__(self) -> str:
        """Safe representation without exposing keys"""
        return f"APIKeyManager(provider={self.provider}, keys={self.get_key_count()}, available={self.get_available_key_count()})"


class MultiProviderKeyManager:
    """
    Manages API keys for multiple AI providers with automatic fallback.
    
    Features:
    - Multi-provider support (OpenAI, Gemini, Anthropic)
    - Automatic provider fallback
    - Thread-safe operations
    - Key rotation per provider
    """
    
    def __init__(self):
        """Initialize multi-provider key manager"""
        self.managers = {}
        self.provider_priority = [AIProvider.OPENAI, AIProvider.GEMINI, AIProvider.ANTHROPIC]
    
    def add_provider(self, provider: AIProvider, keys: List[str]):
        """
        Add API keys for a provider
        
        Args:
            provider: AI provider
            keys: List of API keys
        """
        if keys:
            self.managers[provider] = APIKeyManager(keys, provider)
    
    def get_key(self, provider: AIProvider) -> Optional[str]:
        """
        Get API key for specific provider
        
        Args:
            provider: AI provider
            
        Returns:
            Optional[str]: API key or None if provider not available
        """
        manager = self.managers.get(provider)
        if manager:
            return manager.get_next_key()
        return None
    
    def get_key_with_fallback(self, preferred_provider: AIProvider) -> tuple[Optional[str], Optional[AIProvider]]:
        """
        Get API key with automatic provider fallback
        
        Args:
            preferred_provider: Preferred AI provider
            
        Returns:
            tuple: (api_key, provider) or (None, None) if all providers failed
        """
        # Try preferred provider first
        key = self.get_key(preferred_provider)
        if key:
            return key, preferred_provider
        
        # Fallback to other providers
        for provider in self.provider_priority:
            if provider != preferred_provider:
                key = self.get_key(provider)
                if key:
                    return key, provider
        
        return None, None
    
    def get_all_keys_for_provider(self, provider: AIProvider) -> List[str]:
        """
        Get all keys for a provider (for retry logic)
        
        Args:
            provider: AI provider
            
        Returns:
            List[str]: List of API keys
        """
        manager = self.managers.get(provider)
        if manager:
            return manager.get_all_keys()
        return []
    
    def has_provider(self, provider: AIProvider) -> bool:
        """Check if provider is available"""
        return provider in self.managers
    
    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available providers"""
        return list(self.managers.keys())
    
    def __repr__(self) -> str:
        """Safe representation"""
        providers = ", ".join([f"{p.value}({m.get_key_count()})" for p, m in self.managers.items()])
        return f"MultiProviderKeyManager(providers=[{providers}])"
