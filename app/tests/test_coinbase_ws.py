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
CHANNEL = "ticker"
PRODUCTS = ["BTC-USD"]

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
            
        # Log the entire key file content for debugging
        logger.debug(f"Key file content: {json.dumps(key_data, indent=2, default=str)}")
            
        # Extract API key and private key
        api_key = key_data.get("name", "").split("/")[-1] if key_data.get("name") else None
        private_key_pem = key_data.get("privateKey")
        
        if not api_key or not private_key_pem:
            logger.error("API key or private key not found in the key file")
            return None, None
        
        logger.debug(f"Using API key: {api_key}")
        logger.debug(f"Private key (first 50 chars): {private_key_pem[:50]}...")
        
        # Load the EC private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )
        
        # Extract private key in PKCS8 format for JWT signing
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
            "exp": timestamp + 120,  # 2 minutes expiry
            "iat": timestamp,
            "aud": ["retail_websocket"]  # Required for WebSocket API
        }
        
        # Create JWT header
        header = {
            "alg": "ES256",
            "kid": api_key,
            "typ": "JWT"
        }
        
        # Log what we're about to sign
        logger.debug(f"JWT header: {json.dumps(header, indent=2)}")
        logger.debug(f"JWT payload: {json.dumps(payload, indent=2)}")
        
        # Generate JWT token
        token = jwt.encode(
            payload=payload,
            key=private_bytes.decode('utf-8'),
            algorithm="ES256",
            headers=header
        )
        
        logger.info(f"JWT token generated successfully (length: {len(token)})")
        logger.debug(f"JWT token: {token}")
        
        return token, api_key
        
    except Exception as e:
        logger.error(f"Error generating JWT: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None, None

async def test_ws_authentication():
    logger.info("Starting WebSocket authentication test")
    
    # Generate JWT token
    jwt_token = await generate_jwt()
    
    logger.info(f"JWT token generated successfully (length: {len(jwt_token)})")
    logger.debug(f"JWT token: {jwt_token}")
    
    # Connect to WebSocket
    logger.info(f"Connecting to {WS_URL}")
    async with websockets.connect(WS_URL, logger=logging.getLogger("websockets")) as websocket:
        logger.info("Connected to WebSocket server")
        
        # Authenticate
        auth_message = {"type": "authenticate", "token": jwt_token}
        logger.info(f"Sending authentication message: {json.dumps(auth_message)}")
        await websocket.send(json.dumps(auth_message))
        logger.info("Waiting for authentication response...")
        
        # Send subscription immediately after authentication
        subscription_message = {
            "type": "subscribe",
            "product_ids": PRODUCTS,
            "channel": CHANNEL
        }
        logger.info(f"Sending subscription message: {json.dumps(subscription_message)}")
        await websocket.send(json.dumps(subscription_message))
        logger.info("Waiting for subscription response...")
        
        # Wait for responses (both auth and subscription)
        try:
            for _ in range(2):  # Expect 2 responses: one for auth, one for subscription
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                response_json = json.loads(response)
                logger.info(f"Response received: {json.dumps(response_json, indent=2)}")
                
                # Check if it's an error
                if response_json.get("type") == "error":
                    logger.error(f"Error response: {response_json.get('message')}")
                # Check if it's a subscription confirmation
                elif response_json.get("type") == "subscriptions":
                    logger.info("Subscription confirmed")
                    logger.info(f"Subscribed to: {json.dumps(response_json.get('channels'), indent=2)}")
            
            # Keep connection open for a few seconds to receive some data
            logger.info("Waiting for market data...")
            start_time = time.time()
            message_count = 0
            
            while time.time() - start_time < 10:  # Wait for up to 10 seconds
                try:
                    data = await asyncio.wait_for(websocket.recv(), timeout=1)
                    data_json = json.loads(data)
                    message_count += 1
                    logger.info(f"Market data received ({message_count}): {json.dumps(data_json, indent=2)}")
                except asyncio.TimeoutError:
                    continue
            
            logger.info(f"Received {message_count} market data messages")
            logger.info("WebSocket test completed successfully")
            
        except asyncio.TimeoutError:
            logger.error("Timed out waiting for response")
            return False
        except Exception as e:
            logger.error(f"WebSocket test failed: {str(e)}")
            return False

if __name__ == "__main__":
    logger.info("Starting WebSocket authentication test")
    result = asyncio.run(test_ws_authentication())
    if result:
        logger.info("WebSocket test completed successfully")
    else:
        logger.error("WebSocket test failed") 