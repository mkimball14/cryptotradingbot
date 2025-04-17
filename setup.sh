#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Crypto Trading Bot Setup Script${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for python3
if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check for pip3
if ! command_exists pip3; then
    echo -e "${RED}pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi

# Create and activate virtual environment
echo -e "\n${GREEN}Setting up virtual environment...${NC}"
python3 -m venv venv

# Determine the correct activate script based on OS
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    echo -e "${RED}Unsupported operating system${NC}"
    exit 1
fi

# Upgrade pip
echo -e "\n${GREEN}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install dependencies
echo -e "\n${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt

# Verify installations
echo -e "\n${GREEN}Verifying installations...${NC}"
python -c "import vectorbtpro; import litellm; print('VectorBT Pro and LiteLLM successfully installed!')"

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "source venv/bin/activate  ${GREEN}# On macOS/Linux${NC}"
echo -e "source venv/Scripts/activate  ${GREEN}# On Windows${NC}" 