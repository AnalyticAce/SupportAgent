#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()

async def test_openai_connection():
    """Test OpenAI connection and API key validity"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    if not api_key:
        print("❌ No OpenAI API key found!")
        return False
    
    # Remove quotes if present
    api_key = api_key.strip('\'"')
    
    try:
        client = AsyncOpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use cheaper model for testing
            messages=[{"role": "user", "content": "Say 'Hello World'"}],
            max_tokens=10
        )
        
        print("✅ OpenAI connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        
        # Provide specific error handling
        if "Incorrect API key" in str(e):
            print("💡 Your API key appears to be invalid. Please check:")
            print("   1. The API key is correct")
            print("   2. The API key has not expired")
            print("   3. You have sufficient credits")
        elif "Connection error" in str(e):
            print("💡 Network connection issue. Please check:")
            print("   1. Your internet connection")
            print("   2. Firewall settings")
            print("   3. VPN settings if applicable")
        
        return False

if __name__ == "__main__":
    asyncio.run(test_openai_connection())
