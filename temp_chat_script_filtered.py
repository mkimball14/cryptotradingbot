import vectorbtpro as vbt
import os
import sys
import logging

# Configure logging for the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
script_logger = logging.getLogger("temp_chat_script_filtered")

script_logger.info("Script started.")

# 1. Get API Keys from Environment
openai_api_key = os.getenv('OPENAI_API_KEY')
github_token = os.getenv('GITHUB_TOKEN')

if not openai_api_key:
    script_logger.error("ERROR: OPENAI_API_KEY not found. Please export it.")
    sys.exit(1)
else:
    script_logger.info(f"Using OpenAI API Key: {openai_api_key[:5]}...")

if not github_token:
    script_logger.warning("GITHUB_TOKEN not found, asset finding might fail or be slow.")
else:
    vbt.settings.set('knowledge.assets.vbt.token', github_token)
    script_logger.info("GitHub token configured in vbt.settings.")

# Configure embeddings API key
vbt.settings.set('knowledge.chat.embeddings_configs.openai.api_key', openai_api_key)
script_logger.info("Configured embeddings API key in vbt.settings.")

# 2. Define Search Query and Chat Prompt
search_query = "Enhancements for multi-factor strategy using RSI, BBands, ATR, Volume, Risk Management, Optimization, Regime Adaptation"
chat_prompt = """Based *only* on the provided context about vectorbtpro, suggest enhancements for a multi-factor strategy using RSI, Bollinger Bands, ATR, and Volume. Focus on:
1. Complementary indicators.
2. Signal logic improvements (combining factors, dynamic weights).
3. Advanced risk management (stops, sizing).
4. Optimization techniques (metrics, robustness).
5. Market regime adaptation.
6. Code efficiency tips.
Provide concrete examples or references to VBT functions/classes where possible.
"""

# 3. Find Relevant Assets
try:
    script_logger.info(f"Finding relevant assets for query: '{search_query}'...")
    # Find top 15 relevant items from docs, api, and messages
    relevant_assets = vbt.find_assets(search_query, top_k=15, asset_names=["api", "docs", "messages"])
    script_logger.info(f"Found {len(relevant_assets) if relevant_assets is not None else 0} relevant assets.")

except Exception as e:
    script_logger.error(f"Error during vbt.find_assets: {e}", exc_info=True)
    relevant_assets = None

# 4. Chat with Filtered Assets (if found)
if relevant_assets is not None and len(relevant_assets) > 0:
    try:
        script_logger.info("Running chat on filtered assets...")
        # *** Explicitly pass the API key to .chat() ***
        response = relevant_assets.chat(chat_prompt, api_key=openai_api_key)
        script_logger.info("Chat call completed.")

        print("--- Chat Response ---")
        print(response)
        print("--- End Response ---")

    except Exception as e:
        script_logger.error(f"Error during relevant_assets.chat() call: {e}", exc_info=True)
        print(f"Error during chat call: {e}")
else:
    script_logger.warning("Could not find relevant assets or an error occurred during search. Cannot proceed with chat.")

script_logger.info("Script finished.") 