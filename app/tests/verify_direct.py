import os
import re
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

def read_dotenv_file():
    """Read the .env file directly without using environment variables"""
    env_path = Path(".env")
    if not env_path.exists():
        print(f"Error: .env file not found at {os.path.abspath(env_path)}")
        return None, None
    
    print(f"Reading .env file: {os.path.abspath(env_path)}")
    
    # Read file content
    content = env_path.read_text()
    print(f"Raw file content ({len(content)} bytes):")
    print("-------------------")
    print(content[:200] + "..." if len(content) > 200 else content)
    print("-------------------")
    
    # Parse API key using regex
    api_key_match = re.search(r'COINBASE_API_KEY=([^\n\r"]+)', content)
    api_key = api_key_match.group(1) if api_key_match else None
    
    # Parse API secret using regex - handle multiline
    api_secret_match = re.search(r'COINBASE_API_SECRET=([^\n\r"]+)', content)
    api_secret = api_secret_match.group(1) if api_secret_match else None
    
    return api_key, api_secret

def test_key_loading(api_key, api_secret):
    """Test loading the EC private key directly"""
    if not api_key or not api_secret:
        print("Error: API key or secret not found in .env file")
        return False
    
    print(f"API Key: {api_key}")
    print(f"API Secret (first 20 chars): {api_secret[:20]}...")
    
    try:
        # Add PEM headers if needed
        if not api_secret.startswith("-----BEGIN EC PRIVATE KEY-----"):
            print("Adding PEM headers to API secret")
            pem_data = f"-----BEGIN EC PRIVATE KEY-----\n{api_secret}\n-----END EC PRIVATE KEY-----"
        else:
            pem_data = api_secret
            
        print(f"PEM data (first 50 chars): {pem_data[:50]}...")
            
        # Try to load the key
        try:
            # Try loading PEM format
            private_key = serialization.load_pem_private_key(
                pem_data.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            print("Successfully loaded key as PEM format")
        except Exception as e:
            print(f"Failed to load as PEM: {str(e)}")
            
            # Try loading DER format
            try:
                import base64
                der_data = base64.b64decode(api_secret)
                private_key = serialization.load_der_private_key(
                    der_data,
                    password=None,
                    backend=default_backend()
                )
                print("Successfully loaded key as DER format")
            except Exception as e2:
                print(f"Failed to load as DER: {str(e2)}")
                raise
                
        # Print key details
        if isinstance(private_key, ec.EllipticCurvePrivateKey):
            curve_name = private_key.curve.name
            key_size = private_key.curve.key_size
            print(f"Valid EC private key with curve {curve_name} and size {key_size} bits")
            return True
        else:
            print(f"Loaded key is not an EC private key: {type(private_key)}")
            return False
            
    except Exception as e:
        print(f"Error validating key: {str(e)}")
        return False

if __name__ == "__main__":
    api_key, api_secret = read_dotenv_file()
    test_key_loading(api_key, api_secret) 