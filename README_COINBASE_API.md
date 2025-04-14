# Coinbase Advanced API Integration

This guide explains how to properly set up Coinbase Advanced API authentication for the backtesting scripts.

## Requirements

1. Coinbase Cloud account with access to API key creation (https://cloud.coinbase.com)
2. OpenSSL installed on your system (for key generation)
3. Python 3.6+ with required packages

## Setting Up the API Key

### Method 1: Using the Helper Script (Recommended)

We've provided a helper script that automates the key generation process:

1. Run the helper script:
   ```
   python scripts/generate_coinbase_key.py
   ```

2. The script will:
   - Generate a proper EC key with P-256 curve
   - Save the private key to `keys/coinbase_private.pem`
   - Update the `cdp_api_key.json` file

3. Generate the corresponding public key:
   ```
   openssl ec -in keys/coinbase_private.pem -pubout -out keys/coinbase_public.pem
   ```

4. Go to [Coinbase Cloud Access API](https://cloud.coinbase.com/access/api)

5. Create a new API key:
   - Select the permissions you need (at minimum, read access to products and candles)
   - Choose JWT authentication method
   - Upload the `keys/coinbase_public.pem` file when prompted
   - Copy the key name provided by Coinbase

6. Update the `cdp_api_key.json` file with your actual key name

### Method 2: Manual Setup

If you prefer to set up everything manually:

1. Generate EC private key (MUST be ES256 with P-256 curve):
   ```
   mkdir -p keys
   openssl ecparam -name prime256v1 -genkey -noout -out keys/coinbase_private.pem
   ```

2. Generate public key:
   ```
   openssl ec -in keys/coinbase_private.pem -pubout -out keys/coinbase_public.pem
   ```

3. Go to [Coinbase Cloud Access API](https://cloud.coinbase.com/access/api)

4. Create a new API key with JWT authentication and upload your public key

5. Edit the `cdp_api_key.json` file:
   - Set `key_name` to the name provided by Coinbase
   - Set `private_key` to the full content of your private key file, including the BEGIN/END statements

## Troubleshooting

### Common Errors

1. **Key Deserialization Error**:
   ```
   Could not deserialize key data. The data may be in an incorrect format...
   ```
   - Make sure you're using an EC key with P-256 curve (NOT RSA)
   - Ensure the private key format is correct (begins with `-----BEGIN EC PRIVATE KEY-----`)
   - Check that newlines are preserved in the `cdp_api_key.json` file

2. **Authentication Errors**:
   - Verify the key name matches exactly what Coinbase provided
   - Ensure the public and private keys are a matching pair
   - Check API permissions (needs read access to products)

3. **Date/Time Errors**:
   - Ensure your system clock is accurately synchronized
   - The JWT token uses timestamps and expires 2 minutes after creation

## Advanced Configuration

The Coinbase API integration uses the following:

- ES256 algorithm (ECDSA with P-256 curve and SHA-256) for signing
- JWT token expiration set to 2 minutes
- Issuer set to exactly `"cdp"`
- URI format: `"METHOD host/path"`, e.g., `"GET api.coinbase.com/api/v3/brokerage/products"`

For more details, see the [Coinbase API Documentation](https://docs.cdp.coinbase.com/advanced-trade/docs/rest-api-auth). 