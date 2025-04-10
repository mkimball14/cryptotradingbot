import os
import time
import base64
import hmac
import hashlib
import requests
import json
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.backends import default_backend

def sign_message_with_ec(api_secret, message):
    """Sign a message using EC private key"""
    try:
        # Load the private key
        if not api_secret.startswith("-----BEGIN EC PRIVATE KEY-----"):
            api_secret = f"-----BEGIN EC PRIVATE KEY-----\n{api_secret}\n-----END EC PRIVATE KEY-----"
        
        private_key = serialization.load_pem_private_key(
            api_secret.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # Sign the message
        signature = private_key.sign(
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        
        return base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        print(f"Error signing message: {str(e)}")
        raise

def test_coinbase_jwt():
    """Test if we can generate a valid JWT token for Coinbase"""
    try:
        # Load env variables directly
        load_dotenv()
        api_key = os.getenv('COINBASE_API_KEY')
        api_secret = os.getenv('COINBASE_API_SECRET')
        
        print(f"API Key: {api_key}")
        print(f"API Secret (first 20 chars): {api_secret[:20]}...")
        
        # Check if EC private key is valid
        try:
            # Add PEM headers if they're not already there
            if not api_secret.startswith("-----BEGIN EC PRIVATE KEY-----"):
                print("Adding PEM headers to the private key")
                api_secret = f"-----BEGIN EC PRIVATE KEY-----\n{api_secret}\n-----END EC PRIVATE KEY-----"
            
            # Try to load the private key
            try:
                private_key = serialization.load_pem_private_key(
                    api_secret.encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )
                print("Successfully loaded private key with PEM format")
            except Exception as e:
                print(f"Failed to load key with PEM format: {str(e)}")
                # Try loading as DER encoded
                try:
                    print("Trying to load as DER encoded key...")
                    raw_key = base64.b64decode(api_secret)
                    private_key = serialization.load_der_private_key(
                        raw_key,
                        password=None,
                        backend=default_backend()
                    )
                    print("Successfully loaded DER encoded key")
                except Exception as e2:
                    print(f"Failed to load DER key: {str(e2)}")
                    raise
            
            # Get key details
            if isinstance(private_key, ec.EllipticCurvePrivateKey):
                curve_name = private_key.curve.name
                key_size = private_key.curve.key_size
                print(f"Valid EC private key loaded successfully")
                print(f"Curve: {curve_name}, Key size: {key_size} bits")
                
                # Check if the curve is supported for the signature algorithm
                if curve_name == 'secp256r1' or curve_name == 'P-256':
                    print(f"Curve {curve_name} is compatible with ES256 signature algorithm")
                else:
                    print(f"Warning: Curve {curve_name} might not be compatible with ES256")
                
                # Extract public key
                public_key = private_key.public_key()
                pem_public = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                print(f"Public key (first 50 chars): {pem_public[:50]}...")
                
                return True
            else:
                print("Loaded key is not an EC private key")
                return False
                
        except Exception as e:
            print(f"Error loading private key: {str(e)}")
            return False
    except Exception as e:
        print(f"Error in test: {str(e)}")
        return False

if __name__ == "__main__":
    test_coinbase_jwt() 