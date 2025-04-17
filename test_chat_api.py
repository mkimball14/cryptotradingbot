#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
import vectorbtpro as vbt
from openai import OpenAI

def check_api_keys():
    """Check if the necessary API keys are present in the environment."""
    
    # Load environment variables from .env file
    load_dotenv(verbose=True)
    
    # Check for API keys
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    print(f"OPENROUTER_API_KEY present: {openrouter_api_key is not None}")
    print(f"OPENAI_API_KEY present: {openai_api_key is not None}")
    print(f"GITHUB_TOKEN present: {github_token is not None}")
    
    # Try to inspect vectorbtpro settings
    try:
        print("\nVectorBTPro settings:")
        if hasattr(vbt, 'settings'):
            # Get settings as dict
            settings_dict = {}
            
            # Check knowledge.chat settings
            if hasattr(vbt.settings, 'knowledge') and hasattr(vbt.settings.knowledge, 'chat'):
                settings_dict['knowledge.chat'] = {
                    "openai_key": "**REDACTED**" if hasattr(vbt.settings.knowledge.chat, 'openai_key') else None,
                    "openai_base_url": getattr(vbt.settings.knowledge.chat, 'openai_base_url', None),
                    "model": getattr(vbt.settings.knowledge.chat, 'model', None)
                }
            
            # Check litellm settings
            if hasattr(vbt.settings, 'litellm'):
                settings_dict['litellm'] = {
                    "api_key": "**REDACTED**" if hasattr(vbt.settings.litellm, 'api_key') else None,
                    "api_base": getattr(vbt.settings.litellm, 'api_base', None),
                    "model": getattr(vbt.settings.litellm, 'model', None)
                }
            
            # Print settings
            print(json.dumps(settings_dict, indent=2))
        else:
            print("vbt.settings not found")
    except Exception as e:
        print(f"Error accessing VectorBTPro settings: {e}")
    
    # Try to use OpenAI client directly
    try:
        print("\nTesting OpenAI client:")
        
        # First with OPENAI_API_KEY from environment
        if openai_api_key:
            print("Using OPENAI_API_KEY from environment...")
            client = OpenAI()  # Should use API key from environment
            try:
                # Simple completion test
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello, world!"}],
                    max_tokens=10
                )
                print(f"OpenAI client test successful: {completion.choices[0].message.content}")
            except Exception as e:
                print(f"OpenAI client test failed: {e}")
        
        # Then with OPENROUTER_API_KEY if available
        if openrouter_api_key:
            print("\nUsing OPENROUTER_API_KEY explicitly...")
            try:
                openrouter_client = OpenAI(
                    api_key=openrouter_api_key,
                    base_url="https://openrouter.ai/api/v1"
                )
                completion = openrouter_client.chat.completions.create(
                    model="openrouter/auto",  # Use OpenRouter's auto model
                    messages=[{"role": "user", "content": "Hello, world!"}],
                    max_tokens=10
                )
                print(f"OpenRouter client test successful: {completion.choices[0].message.content}")
            except Exception as e:
                print(f"OpenRouter client test failed: {e}")
    except Exception as e:
        print(f"Error testing OpenAI client: {e}")
    
    # Try using vectorbtpro's chat function
    try:
        print("\nTesting vectorbtpro.chat:")
        if hasattr(vbt, 'chat') and callable(vbt.chat):
            # Set OPENAI_API_KEY environment variable explicitly if not set
            if not os.environ.get("OPENAI_API_KEY") and openrouter_api_key:
                print("Setting OPENAI_API_KEY from OPENROUTER_API_KEY for vbt.chat test")
                os.environ["OPENAI_API_KEY"] = openrouter_api_key
            
            try:
                # Test vbt.chat function
                response = vbt.chat("Hello, world!")
                print(f"vbt.chat test successful: {response}")
            except Exception as e:
                print(f"vbt.chat test failed: {e}")
        else:
            print("vbt.chat function not available")
    except Exception as e:
        print(f"Error testing vectorbtpro.chat: {e}")

if __name__ == "__main__":
    check_api_keys() 