import vectorbtpro as vbt
import os
import sys
import logging

# Configure logging for the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
script_logger = logging.getLogger("temp_chat_script")

script_logger.info("Script started.")

# 1. Get API Key from Environment
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    script_logger.error("ERROR: OPENAI_API_KEY not found in environment. Please export it first.")
    sys.exit(1)
else:
    script_logger.info(f"Using API Key from env: {openai_api_key[:5]}...")

# 2. Define the Prompt
prompt = """Analyze the following multi-factor trading strategy implemented using vectorbtpro and suggest specific enhancements:

Current Strategy Summary:
- Indicators: Volatility Regime (rolling std vs MA), Consolidation Breakout (HL range vs MA, rolling min/max), Volume Divergence (volume vs MA, confirms breakouts), Market Microstructure (candle shadows).
- Signal Generation: Weighted sum of factor scores (long/short separate). Entries when score > 0.5.
- Risk Management: ATR-based SL distance used for position sizing (fixed risk fraction). Optional fixed TP % and TSL %. Size type is 'Amount'.
- Optimization: Parameter grid search (WFO or single run) optimizing metrics like Sharpe Ratio.

Request for Enhancements:
Based on the vectorbtpro documentation and best practices, please suggest improvements in the following areas:
1.  Additional Indicators: What other VBT indicators could complement or improve the existing factors (e.g., momentum, trend, mean-reversion)?
2.  Signal Logic: Are there better ways to combine factor scores or generate entry/exit signals (e.g., machine learning, different thresholding)? How to dynamically adjust factor weights?
3.  Risk Management: Suggest more advanced stop-loss (e.g., chandelier), take-profit, or position sizing techniques available in VBT (beyond fixed % or ATR multiple).
4.  Optimization: Recommend alternative optimization metrics or techniques supported by VBT for robustness (e.g., Sortino, Calmar, handling walk-forward optimization results)?
5.  Market Regime Adaptation: How can the strategy logic (parameters, weights, risk) be adapted dynamically to different market regimes (trending vs. ranging) using VBT features?
6.  Code Efficiency: Are there specific VBT functions or techniques to make the indicator calculation or backtesting loop more efficient?

Provide concrete examples or references to VBT functions/classes where possible.
"""

# 3. Configure vectorbtpro settings (optional but good practice)
# Note: We still pass api_key explicitly because env var wasn't reliable before
# You might remove the api_key argument to vbt.chat if vbt.settings works reliably in a full script.
github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    vbt.settings.set('knowledge.assets.vbt.token', github_token)
    script_logger.info("GitHub token configured in vbt.settings.")
else:
    script_logger.warning("GITHUB_TOKEN not found, asset pulling might fail.")

# Configure embeddings to use the API key as well
vbt.settings.set('knowledge.chat.embeddings_configs.openai.api_key', openai_api_key)
script_logger.info("Configured embeddings API key in vbt.settings.")

# 4. Run vbt.chat()
try:
    script_logger.info("Running vbt.chat()...")
    # *** Explicitly pass the API key ***
    response = vbt.chat(prompt, api_key=openai_api_key)
    script_logger.info("vbt.chat() call completed.")

    print("--- Chat Response ---")
    print(response)
    print("--- End Response ---")

except Exception as e:
    script_logger.error(f"Error during vbt.chat() call: {e}", exc_info=True)
    print(f"Error during vbt.chat() call: {e}")

script_logger.info("Script finished.") 