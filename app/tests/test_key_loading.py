import os
import json
import base64
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_key_from_json():
    """Test loading the private key directly from the JSON file"""
    try:
        # Check if the JSON file exists
        json_file = "cdp_api_key (3).json"
        if not os.path.exists(json_file):
            logger.error(f"File not found: {json_file}")
            return False
            
        # Load the API key file
        with open(json_file, "r") as f:
            key_data = json.load(f)
            
        # Extract the key properties
        api_key = key_data.get("name", "").split("/")[-1] if key_data.get("name") else None
        private_key_pem = key_data.get("privateKey")
        
        if not api_key:
            logger.error("API key not found in JSON file")
            return False
            
        if not private_key_pem:
            logger.error("Private key not found in JSON file")
            return False
            
        logger.info(f"API Key: {api_key}")
        logger.info(f"Private Key format: {private_key_pem[:40]}...")
        
        # Try to load the private key
        try:
            # Load the EC private key
            key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            
            # Get the curve details
            if isinstance(key, ec.EllipticCurvePrivateKey):
                curve_name = key.curve.name
                key_size = key.curve.key_size
                logger.info(f"✅ Key loaded successfully - type: {type(key)}")
                logger.info(f"✅ Curve: {curve_name}, size: {key_size} bits")
                
                # Get PEM format for JWT
                private_bytes = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                logger.info(f"✅ Private key in PKCS8 format (first 50 chars): {private_bytes[:50]}...")
                
                # Get the public key for verification
                public_key = key.public_key()
                public_bytes = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                logger.info(f"✅ Public key (first 50 chars): {public_bytes[:50]}...")
                
                return True
            else:
                logger.error(f"❌ Not an EC key: {type(key)}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to load key: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing key: {str(e)}")
        return False

def test_key_from_env():
    """Test loading the private key from environment variable"""
    try:
        # Load from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get API key and secret
        api_key = os.getenv("COINBASE_API_KEY")
        api_secret = os.getenv("COINBASE_API_SECRET")
        
        if not api_key:
            logger.error("API key not found in environment")
            return False
            
        if not api_secret:
            logger.error("API secret not found in environment")
            return False
            
        logger.info(f"API Key: {api_key}")
        logger.info(f"API Secret format: {api_secret[:40]}...")
        
        # Ensure the secret has PEM headers
        if not api_secret.startswith("-----BEGIN EC PRIVATE KEY-----"):
            logger.info("Adding PEM headers to API secret")
            api_secret = f"-----BEGIN EC PRIVATE KEY-----\n{api_secret}\n-----END EC PRIVATE KEY-----"
        
        # Try to load the private key
        try:
            # Load the EC private key
            key = serialization.load_pem_private_key(
                api_secret.encode(),
                password=None,
                backend=default_backend()
            )
            
            # Get the curve details
            if isinstance(key, ec.EllipticCurvePrivateKey):
                curve_name = key.curve.name
                key_size = key.curve.key_size
                logger.info(f"✅ Key loaded successfully - type: {type(key)}")
                logger.info(f"✅ Curve: {curve_name}, size: {key_size} bits")
                
                # Get PEM format for JWT
                private_bytes = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                logger.info(f"✅ Private key in PKCS8 format (first 50 chars): {private_bytes[:50]}...")
                
                return True
            else:
                logger.error(f"❌ Not an EC key: {type(key)}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to load key: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing key: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n=== Testing key loading from JSON file ===")
    json_result = test_key_from_json()
    
    print("\n=== Testing key loading from .env file ===")
    env_result = test_key_from_env()
    
    if json_result and env_result:
        print("\n✅ All tests passed! The key is properly formatted and loadable.")
    else:
        print("\n❌ Some tests failed. Check the errors above.") 