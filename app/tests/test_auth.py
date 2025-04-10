import os
import json
import asyncio
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define the path to the key file
KEY_FILE = "cdp_api_key (3).json"

async def test_jwt_generation():
    """Test the JWT token generation and formatting."""
    try:
        # Check if key file exists
        if not os.path.exists(KEY_FILE):
            logger.error(f"API key file not found: {KEY_FILE}")
            logger.error("Make sure the API key file is in the project root directory.")
            return
            
        logger.info(f"Using API key file: {os.path.abspath(KEY_FILE)}")
        
        # Load keys from JSON file
        with open(KEY_FILE, 'r') as f:
            key_data = json.load(f)
            
        # Extract API key and private key
        api_key = key_data.get("name", "").split("/")[-1] if key_data.get("name") else None
        private_key_pem = key_data.get("privateKey")
        
        if not api_key or not private_key_pem:
            logger.error("API key or private key not found in the key file")
            return
            
        logger.info(f"API Key: {api_key}")
        logger.info(f"Private Key format: {private_key_pem[:40]}...")
        
        # 1. Test loading the private key
        try:
            # Import JWT here to avoid import issues
            import jwt
            
            # Load the EC private key
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            
            # Get key details
            if isinstance(private_key, ec.EllipticCurvePrivateKey):
                curve_name = private_key.curve.name
                key_size = private_key.curve.key_size
                logger.info(f"✅ Valid EC private key - curve: {curve_name}, size: {key_size} bits")
                
                # Extract private key in PKCS8 format for JWT signing
                private_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                logger.info(f"✅ Private key in PKCS8 format (first 50 chars): {private_bytes[:50]}...")
                
                # 2. Generate JWT token
                import time
                
                # Create JWT payload
                timestamp = int(time.time())
                payload = {
                    "sub": api_key,
                    "iss": "coinbase-cloud",
                    "nbf": timestamp,
                    "exp": timestamp + 60,
                    "iat": timestamp,
                    "aud": ["retail_websocket"]
                }
                
                # Create JWT header
                header = {
                    "alg": "ES256",
                    "kid": api_key,
                    "typ": "JWT"
                }
                
                logger.info(f"JWT Header: {json.dumps(header)}")
                logger.info(f"JWT Payload: {json.dumps(payload)}")
                
                # Generate JWT token
                token = jwt.encode(
                    payload=payload,
                    key=private_bytes.decode('utf-8'),
                    algorithm="ES256",
                    headers=header
                )
                
                logger.info(f"✅ JWT token generated successfully")
                logger.info(f"JWT token length: {len(token)} characters")
                logger.info(f"JWT token: {token[:50]}...")
                
                # 3. Prepare authentication message
                auth_message = {
                    "type": "subscribe",
                    "channel": "heartbeat",
                    "product_ids": ["BTC-USD"],
                    "jwt": token
                }
                
                logger.info(f"Authentication message: {json.dumps(auth_message, indent=2)}")
                
                return True
            else:
                logger.error(f"❌ Not an EC key: {type(private_key)}")
                return False
        except Exception as e:
            logger.error(f"❌ Error generating JWT: {str(e)}")
            return False
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_jwt_generation()) 