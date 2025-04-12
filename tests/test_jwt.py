from coinbase import jwt_generator
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API credentials from environment - use them directly
    api_key = os.getenv("COINBASE_API_KEY").strip('"\'')
    api_secret = os.getenv("COINBASE_API_SECRET").strip('"\'')
    
    # Test parameters
    request_method = "GET"
    request_path = "/ws/heartbeat"
    
    try:
        # Generate JWT token
        jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
        print(f"JWT URI: {jwt_uri}")
        print(f"Using API Key: {api_key}")
        print(f"API Secret format:\n{api_secret}")
        
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)
        print(f"\nGenerated JWT token: {jwt_token}")
        
    except Exception as e:
        print(f"Error generating JWT token: {str(e)}")
        print("\nPlease ensure your API key and secret are generated from https://cloud.coinbase.com/access/api")
        print("The API secret should be in the format: MIHcAgEBBEIB...")

if __name__ == "__main__":
    main() 