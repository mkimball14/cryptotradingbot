"""
automated_strategy_improver.py

A persistent automation loop for continuous WFO analysis, enhancement, and self-improvement of the trading strategy.

- Monitors for new WFO results
- Analyzes performance and overtrading
- Applies logic/parameter enhancements
- Logs/documentation
- Triggers next WFO run
- Designed for hands-off, self-improving research
"""
import os
import time
import pandas as pd
from datetime import datetime
import subprocess

PROGRESS_LOG = "../docs/PROGRESS_LOG.md"
NEXT_STEPS = "../docs/NEXT_STEPS.md"
WFO_RESULTS = "../data/results/wfo_results.csv"
WFO_RUNNER = "./scripts/strategies/refactored_edge/wfo_runner.py"
CHECK_INTERVAL = 60  # seconds

# --- Utility: Log to markdown files ---
def append_to_log(filename, text):
    with open(filename, "a") as f:
        f.write(f"\n{text}\n")

def analyze_results(results_path):
    if not os.path.exists(results_path):
        return None
    df = pd.read_csv(results_path)
    if df.empty:
        return None
    # Find best and worst param sets, trade counts, returns, etc.
    best = df.sort_values(by="test_return", ascending=False).iloc[0]
    worst = df.sort_values(by="test_return", ascending=True).iloc[0]
    overtrading = df.loc[df[["long_trades","short_trades"]].max(axis=1) > 1000]
    summary = {
        "best": best.to_dict(),
        "worst": worst.to_dict(),
        "overtrading_count": len(overtrading),
        "mean_test_return": df["test_return"].mean(),
        "median_trades": df[["long_trades","short_trades"]].sum(axis=1).median(),
    }
    return summary

def enhance_strategy_logic(summary):
    """
    Stub: This is where you would programmatically update strategy logic or parameters.
    For now, just logs what would be changed.
    """
    # Example: if overtrading_count > 0, restrict entries further
    actions = []
    if summary and summary["overtrading_count"] > 0:
        actions.append("Restrict entry logic: add more filters or raise thresholds.")
    if summary and summary["mean_test_return"] < 0:
        actions.append("Tighten risk management or add regime/volatility filter.")
    if not actions:
        actions.append("No major changes needed. Continue loop.")
    return actions

def run_wfo():
    # Launch the WFO runner script and wait for completion
    print(f"[{datetime.now()}] Launching WFO runner...")
    result = subprocess.run(["python3", WFO_RUNNER], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"WFO runner failed: {result.stderr}")
    return result.returncode == 0

def main():
    print("Starting Automated Strategy Improver Loop...")
    last_results_time = None
    while True:
        # Step 1: Wait for new WFO results
        if os.path.exists(WFO_RESULTS):
            mod_time = os.path.getmtime(WFO_RESULTS)
            if last_results_time is None or mod_time > last_results_time:
                print(f"[{datetime.now()}] New WFO results detected. Analyzing...")
                summary = analyze_results(WFO_RESULTS)
                if summary:
                    log_entry = f"### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n- Best test return: {summary['best']['test_return']:.2f}%\n- Worst: {summary['worst']['test_return']:.2f}%\n- Overtrading param sets: {summary['overtrading_count']}\n- Mean test return: {summary['mean_test_return']:.2f}%\n- Median trades: {summary['median_trades']}"
                    append_to_log(PROGRESS_LOG, log_entry)
                    actions = enhance_strategy_logic(summary)
                    for action in actions:
                        append_to_log(NEXT_STEPS, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}")
                    print(f"Logged analysis and next steps. Actions: {actions}")
                else:
                    print("No results to analyze.")
                last_results_time = mod_time
        # Step 2: Run WFO
        run_wfo()
        # Step 3: Wait before next iteration
        print(f"[{datetime.now()}] Sleeping {CHECK_INTERVAL}s before next loop...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
