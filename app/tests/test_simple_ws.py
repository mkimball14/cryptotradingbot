import os
import json
import asyncio
import logging
import websockets
import time
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define constants
WS_URL = "wss://advanced-trade-ws.coinbase.com"
KEY_FILE = "cdp_api_key (3).json"

async def generate_jwt():
    """Generate a JWT token from the key file"""
    try:
        # Check if key file exists
        if not os.path.exists(KEY_FILE):
            logger.error(f"API key file not found: {KEY_FILE}")
            return None, None
            
        # Load keys from JSON file
        with open(KEY_FILE, 'r') as f:
            key_data = json.load(f)
            
        # Extract API key and private key
        api_key = key_data.get("name", "").split("/")[-1] if key_data.get("name") else None
        private_key_pem = key_data.get("privateKey")
        
        if not api_key or not private_key_pem:
            logger.error("API key or private key not found in the key file")
            return None, None
        
        # Load the EC private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )
        
        # Get private key in PKCS8 format for JWT signing
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
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
        
        # Generate JWT token
        token = jwt.encode(
            payload=payload,
            key=private_bytes.decode('utf-8'),
            algorithm="ES256",
            headers=header
        )
        
        logger.info(f"JWT token generated successfully (length: {len(token)})")
        return token, api_key
        
    except Exception as e:
        logger.error(f"Error generating JWT: {str(e)}")
        return None, None

async def test_websocket():
    """Test WebSocket connection with authentication and subscription"""
    try:
        # Generate JWT token
        token, api_key = await generate_jwt()
        if not token or not api_key:
            logger.error("Failed to generate JWT token")
            return False
        
        logger.info(f"Connecting to {WS_URL}")
        
        # Connect to WebSocket
        async with websockets.connect(WS_URL) as websocket:
            logger.info("Connected to WebSocket server")
            
            # Prepare authentication message
            auth_message = {
                "type": "subscribe",
                "channel": "heartbeat",
                "product_ids": ["BTC-USD"],
                "jwt": token
            }
            
            logger.info("Sending authentication message")
            await websocket.send(json.dumps(auth_message))
            
            # Wait for response
            logger.info("Waiting for authentication response...")
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            logger.info(f"Received response: {json.dumps(response_data, indent=2)}")
            
            # Check for successful authentication
            if response_data.get("type") == "error":
                logger.error(f"Authentication failed: {response_data.get('message')}")
                return False
            
            if "subscriptions" in response_data:
                logger.info("Authentication successful via subscription response")
                
                # Wait for a few heartbeat messages
                logger.info("Waiting for messages...")
                message_count = 0
                max_messages = 3
                try:
                    while message_count < max_messages:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                        message_data = json.loads(message)
                        logger.info(f"Received message {message_count+1}: {json.dumps(message_data, indent=2)}")
                        message_count += 1
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for messages")
                
                return True
            
            logger.warning(f"Unexpected response type: {response_data.get('type')}")
            return False
            
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"WebSocket connection closed: {str(e)}")
        return False
    except asyncio.TimeoutError:
        logger.error("Timeout connecting to WebSocket server")
        return False
    except Exception as e:
        logger.error(f"Error in WebSocket test: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting WebSocket test")
    result = asyncio.run(test_websocket())
    if result:
        logger.info("WebSocket test completed successfully")
    else:
        logger.error("WebSocket test failed") 