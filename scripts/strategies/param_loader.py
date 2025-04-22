#!/usr/bin/env python3
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("param_loader")

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = ROOT_DIR / "config"
DEFAULT_PARAMS_FILE = CONFIG_DIR / "strategy_params.json"

def load_strategy_params(
    profile_name: str = "optimized_hourly",
    params_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load strategy parameters from a JSON configuration file.
    
    Args:
        profile_name: The name of the parameter profile to load
        params_file: Optional custom path to the parameters file
        
    Returns:
        Dictionary containing the strategy parameters
    """
    file_path = params_file if params_file else DEFAULT_PARAMS_FILE
    
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Parameters file {file_path} not found.")
            return get_fallback_params()
        
        with open(file_path, 'r') as f:
            all_params = json.load(f)
        
        if profile_name not in all_params:
            logger.warning(f"Profile '{profile_name}' not found in parameters file. Available profiles: {list(all_params.keys())}")
            # Fall back to first profile in the file or default params
            if len(all_params) > 0:
                first_profile = next(iter(all_params))
                logger.info(f"Using '{first_profile}' profile instead.")
                return all_params[first_profile]
            else:
                return get_fallback_params()
        
        params = all_params[profile_name]
        logger.info(f"Loaded '{profile_name}' parameter profile successfully.")
        return params
    
    except Exception as e:
        logger.error(f"Error loading strategy parameters: {e}")
        return get_fallback_params()

def list_available_profiles(params_file: Optional[str] = None) -> List[str]:
    """
    List all available parameter profiles in the configuration file.
    
    Args:
        params_file: Optional custom path to the parameters file
        
    Returns:
        List of profile names
    """
    file_path = params_file if params_file else DEFAULT_PARAMS_FILE
    
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Parameters file {file_path} not found.")
            return []
        
        with open(file_path, 'r') as f:
            all_params = json.load(f)
        
        profiles = list(all_params.keys())
        return profiles
    
    except Exception as e:
        logger.error(f"Error listing parameter profiles: {e}")
        return []

def get_profile_description(profile_name: str, params_file: Optional[str] = None) -> str:
    """
    Get the description for a specific parameter profile.
    
    Args:
        profile_name: The name of the parameter profile
        params_file: Optional custom path to the parameters file
        
    Returns:
        Profile description or empty string if not found
    """
    file_path = params_file if params_file else DEFAULT_PARAMS_FILE
    
    try:
        if not os.path.exists(file_path):
            return ""
        
        with open(file_path, 'r') as f:
            all_params = json.load(f)
        
        if profile_name in all_params and "description" in all_params[profile_name]:
            return all_params[profile_name]["description"]
        return ""
    
    except Exception as e:
        logger.error(f"Error getting profile description: {e}")
        return ""

def get_fallback_params() -> Dict[str, Any]:
    """
    Return fallback parameters in case the config file is not found or has errors.
    
    Returns:
        Dictionary containing default fallback parameters
    """
    logger.warning("Using fallback parameters.")
    return {
        "lookback_window": 20,
        "vol_filter_window": 100,
        "volatility_threshold": 0.5,
        "signal_threshold": 0.3,
        "default_factor_weights": {
            "volatility_regime": 0.25,
            "consolidation_breakout": 0.25,
            "volume_divergence": 0.25,
            "market_microstructure": 0.25
        }
    }

if __name__ == "__main__":
    # Test the parameter loader
    print("\nAvailable Parameter Profiles:")
    profiles = list_available_profiles()
    
    for profile in profiles:
        desc = get_profile_description(profile)
        print(f"- {profile}: {desc}")
    
    print("\nLoading 'optimized_hourly' profile:")
    params = load_strategy_params("optimized_hourly")
    print(json.dumps(params, indent=2)) 