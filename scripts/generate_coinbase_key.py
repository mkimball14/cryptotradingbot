#!/usr/bin/env python
"""
Coinbase Advanced API Key Generator

This script helps generate the correct EC key format for Coinbase Advanced API
and updates the cdp_api_key.json file with proper credentials.

Requirements:
- OpenSSL installed on your system
- Python 3.6+
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def generate_ec_key():
    """Generate an EC private key using OpenSSL"""
    print("Generating EC private key (ES256 with P-256 curve)...")
    
    # Ensure the keys directory exists
    keys_dir = Path("./keys")
    keys_dir.mkdir(exist_ok=True)
    
    private_key_path = keys_dir / "coinbase_private.pem"
    
    # Command to generate EC private key using P-256 curve (prime256v1)
    cmd = ["openssl", "ecparam", "-name", "prime256v1", "-genkey", "-noout", "-out", str(private_key_path)]
    
    try:
        # Run the OpenSSL command
        subprocess.run(cmd, check=True)
        print(f"Private key generated successfully at: {private_key_path}")
        
        # Read the generated key
        with open(private_key_path, 'r') as f:
            private_key = f.read()
            
        return private_key
    except subprocess.CalledProcessError as e:
        print(f"Error generating private key: {e}")
        print("Make sure OpenSSL is installed on your system.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def update_credentials_file(private_key, key_name=None):
    """Update the cdp_api_key.json file with the new credentials"""
    creds_file = Path("./cdp_api_key.json")
    
    # Create default structure
    creds = {
        "_README": "This file contains Coinbase Advanced API credentials for JWT authentication. Follow the instructions below to set up your API keys correctly.",
        "_INSTRUCTIONS": [
            "1. Go to https://cloud.coinbase.com/access/api to create a new API key",
            "2. Generate an EC private key using the CORRECT format (MUST be ES256 with P-256 curve)",
            "3. To generate a proper key, use the following command:",
            "   openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem",
            "4. The key MUST be in EC format (not RSA)",
            "5. Copy your key_name from Coinbase Cloud",
            "6. Paste the FULL private key including the BEGIN/END statements",
            "7. Make sure newlines are preserved (use \\n if editing manually)"
        ]
    }
    
    # Load existing file if it exists
    if creds_file.exists():
        try:
            with open(creds_file, 'r') as f:
                existing_creds = json.load(f)
                # Preserve existing values that aren't being updated
                for key, value in existing_creds.items():
                    if key not in ["private_key"] and (key_name is None and key != "key_name"):
                        creds[key] = value
        except json.JSONDecodeError:
            print("Warning: Existing credentials file is not valid JSON, creating new file.")
    
    # Update the credentials
    if private_key:
        creds["private_key"] = private_key
    
    if key_name:
        creds["key_name"] = key_name
    elif "key_name" not in creds:
        creds["key_name"] = "YOUR_COINBASE_API_KEY_NAME"
    
    # Write the updated credentials
    with open(creds_file, 'w') as f:
        json.dump(creds, f, indent=4)
    
    print(f"Credentials file updated: {creds_file}")
    if creds["key_name"] == "YOUR_COINBASE_API_KEY_NAME":
        print("NOTE: You still need to update 'key_name' with your actual Coinbase API key name")

def main():
    """Main function"""
    print("Coinbase Advanced API Key Generator")
    print("==================================")
    print("This script will generate a proper EC private key for Coinbase Advanced API authentication.")
    
    # Check if OpenSSL is installed
    try:
        subprocess.run(["openssl", "version"], stdout=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: OpenSSL is not installed or not in PATH.")
        print("Please install OpenSSL and try again.")
        sys.exit(1)
    
    # Generate the key
    private_key = generate_ec_key()
    if not private_key:
        print("Failed to generate private key. Exiting.")
        sys.exit(1)
    
    # Ask for key name
    print("\nDo you want to enter your Coinbase API key name now?")
    answer = input("Enter 'y' for yes, any other key to skip: ").strip().lower()
    
    key_name = None
    if answer == 'y':
        key_name = input("Enter your Coinbase API key name: ").strip()
    
    # Update the credentials file
    update_credentials_file(private_key, key_name)
    
    print("\nIMPORTANT NEXT STEPS:")
    print("1. Go to https://cloud.coinbase.com/access/api")
    print("2. Create a new API key")
    print("3. When prompted for a public key, generate one from your private key using:")
    print("   openssl ec -in keys/coinbase_private.pem -pubout -out keys/coinbase_public.pem")
    print("4. Upload the generated public key file to Coinbase")
    print("5. Make sure to copy the key name from Coinbase and update it in cdp_api_key.json")
    print("\nYour backtest script should now work with the Coinbase API!")

if __name__ == "__main__":
    main() 