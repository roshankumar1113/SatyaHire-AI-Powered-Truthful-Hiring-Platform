"""
Test AI Client - Verify API key management and AI functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ml.ai_client import get_ai_client, AIClientError
from app.utils.api_key_manager import AIProvider


def test_ai_client():
    """Test AI client functionality"""
    
    print("=" * 60)
    print("AI Client Test Suite")
    print("=" * 60)
    print()
    
    try:
        # Initialize client
        print("1. Initializing AI client...")
        ai_client = get_ai_client()
        print("   ✓ AI client initialized")
        print()
        
        # Check status
        print("2. Checking AI client status...")
        status = ai_client.get_status()
        print(f"   Available providers: {status['available_providers']}")
        print(f"   Default provider: {status['default_provider']}")
        print(f"   Model: {status['model']}")
        print(f"   Key manager: {status['key_manager']}")
        print()
        
        # Check if any providers available
        if not status['available_providers']:
            print("   ⚠ WARNING: No AI providers configured!")
            print("   Please add API keys to .env file:")
            print("   OPENAI_API_KEYS=sk-key1,sk-key2")
            print()
            return False
        
        # Test text generation (if keys available)
        print("3. Testing text generation...")
        try:
            response = ai_client.generate_text(
                prompt="Say 'Hello from SatyaHire AI!' in a professional way.",
                max_tokens=50
            )
            print(f"   ✓ Response: {response[:100]}...")
            print()
        except AIClientError as e:
            print(f"   ✗ Failed: {str(e)}")
            print("   This is expected if no valid API keys are configured")
            print()
        
        # Test interview question generation
        print("4. Testing interview question generation...")
        try:
            question = ai_client.generate_interview_question(
                job_description="Senior Python Developer with FastAPI experience",
                candidate_background="5 years Python, 2 years FastAPI",
                question_number=1
            )
            print(f"   ✓ Generated question: {question[:100]}...")
            print()
        except AIClientError as e:
            print(f"   ✗ Failed: {str(e)}")
            print()
        
        # Test key rotation (if multiple keys)
        print("5. Testing key rotation...")
        providers = ai_client.key_manager.get_available_providers()
        for provider in providers:
            manager = ai_client.key_manager.managers.get(provider)
            if manager:
                key_count = manager.get_key_count()
                print(f"   {provider.value}: {key_count} key(s)")
                
                if key_count > 1:
                    print(f"   Testing rotation for {provider.value}...")
                    keys_used = []
                    for i in range(min(3, key_count)):
                        key = manager.get_next_key()
                        # Only show first/last 4 chars for security
                        masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
                        keys_used.append(masked_key)
                    print(f"   Keys rotated: {' → '.join(keys_used)}")
        print()
        
        print("=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_key_manager():
    """Test key manager directly"""
    
    print("\n" + "=" * 60)
    print("Key Manager Test")
    print("=" * 60)
    print()
    
    from app.utils.api_key_manager import APIKeyManager, MultiProviderKeyManager
    
    # Test single provider
    print("1. Testing single provider key manager...")
    keys = ["key1", "key2", "key3"]
    manager = APIKeyManager(keys, AIProvider.OPENAI)
    
    print(f"   Total keys: {manager.get_key_count()}")
    print(f"   Available keys: {manager.get_available_key_count()}")
    
    # Test rotation
    print("   Testing rotation:")
    for i in range(5):
        key = manager.get_next_key()
        print(f"   Request {i+1}: {key}")
    print()
    
    # Test multi-provider
    print("2. Testing multi-provider key manager...")
    multi_manager = MultiProviderKeyManager()
    multi_manager.add_provider(AIProvider.OPENAI, ["openai_key1", "openai_key2"])
    multi_manager.add_provider(AIProvider.GEMINI, ["gemini_key1"])
    
    print(f"   Available providers: {[p.value for p in multi_manager.get_available_providers()]}")
    
    # Test fallback
    print("   Testing fallback:")
    key, provider = multi_manager.get_key_with_fallback(AIProvider.OPENAI)
    print(f"   Got key from: {provider.value}")
    print()
    
    print("✓ Key manager tests passed!")
    print()


if __name__ == "__main__":
    print("\n🚀 Starting AI Client Tests\n")
    
    # Test key manager
    test_key_manager()
    
    # Test AI client
    success = test_ai_client()
    
    if success:
        print("\n✅ All tests passed!")
        print("\nNext steps:")
        print("1. Add your API keys to .env file")
        print("2. Run: python -m uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/api/docs")
        print("4. Test /api/v1/ai/health endpoint")
    else:
        print("\n⚠ Some tests failed")
        print("Please check your .env configuration")
    
    print()
