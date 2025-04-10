import os
from dotenv import load_dotenv

def print_env():
    # Load .env file
    load_dotenv()
    
    # Print environment variables
    print("=== Environment Variables ===")
    print(f"COINBASE_API_KEY: {os.getenv('COINBASE_API_KEY')}")
    
    # Get API secret but don't print the whole thing for security
    api_secret = os.getenv('COINBASE_API_SECRET')
    if api_secret:
        print(f"COINBASE_API_SECRET length: {len(api_secret)}")
        print(f"COINBASE_API_SECRET first 20 chars: {api_secret[:20]}...")
        print(f"COINBASE_API_SECRET is quoted: {api_secret.startswith('"') and api_secret.endswith('"')}")
    else:
        print("COINBASE_API_SECRET: Not found")
    
    # Print all environment variables
    print("\n=== All Environment Variables ===")
    env_vars = {}
    for key, value in os.environ.items():
        if key.startswith("COINBASE_"):
            # Truncate for security
            if "SECRET" in key or "KEY" in key:
                env_vars[key] = f"{value[:10]}..." if value else "None"
            else:
                env_vars[key] = value
    
    for key, value in sorted(env_vars.items()):
        print(f"{key}: {value}")

if __name__ == "__main__":
    print_env() 