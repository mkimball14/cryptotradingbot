#!/bin/bash

# Run Strategy Script
# This script runs the cryptocurrency factor-based strategy

echo "Starting Crypto Factor-Based Strategy..."

# Set the Python path to include the crypto_factor_strategy directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the main script
python main.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Strategy execution completed successfully!"
else
    echo "Strategy execution failed with error code $?"
fi

# Optional: Add timestamp to the end
echo "Run completed at $(date)" 