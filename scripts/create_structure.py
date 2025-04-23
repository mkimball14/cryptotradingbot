#!/usr/bin/env python3
"""
Create directory structure for the crypto trading bot.
"""

import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_directory_structure():
    """Create all required directories for the project."""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Define directories to create
    directories = [
        os.path.join(script_dir, 'data'),
        os.path.join(script_dir, 'indicators'),
        os.path.join(script_dir, 'portfolio'),
        os.path.join(script_dir, 'strategies'),
        os.path.join(script_dir, 'utils'),
        os.path.join(script_dir, 'api'),
        os.path.join(script_dir, 'config'),
        os.path.join(script_dir, 'tests'),
        os.path.join(project_root, 'data'),
        os.path.join(project_root, 'logs'),
        os.path.join(project_root, 'models'),
        os.path.join(project_root, 'results')
    ]
    
    # Create each directory if it doesn't exist
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        else:
            logger.info(f"Directory already exists: {directory}")
            
    # Create __init__.py files in each directory
    for directory in directories:
        if directory.startswith(script_dir):
            init_file = os.path.join(directory, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('"""' + os.path.basename(directory) + ' package."""\n')
                logger.info(f"Created __init__.py in {directory}")

if __name__ == "__main__":
    logger.info("Creating directory structure...")
    create_directory_structure()
    logger.info("Directory structure created successfully!") 