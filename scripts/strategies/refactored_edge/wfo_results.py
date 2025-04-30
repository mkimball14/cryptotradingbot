"""
Result processing and reporting functions for Walk-Forward Optimization (WFO).

This module handles saving, formatting, and analyzing WFO results, including CSV exports,
performance metrics calculations, and summary report generation.
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Local imports
from scripts.strategies.refactored_edge.wfo_utils import OUTPUT_DIR, RESULTS_FILENAME, ensure_output_dir


def initialize_results_storage():
    """
    Initialize directory structure for saving results.
    
    Returns:
        str: Path to the results directory
    """
    results_dir = ensure_output_dir()
    
    # Create additional subdirectories if needed
    regime_eval_dir = os.path.join(results_dir, "regime_evaluation")
    os.makedirs(regime_eval_dir, exist_ok=True)
    
    return results_dir


def save_wfo_results(results_list, output_dir=None, filename=None):
    """
    Save WFO results to a CSV file.
    
    Args:
        results_list (list): List of result dictionaries
        output_dir (str, optional): Directory to save results. Defaults to OUTPUT_DIR.
        filename (str, optional): Filename for results. Defaults to RESULTS_FILENAME.
        
    Returns:
        str: Path to the saved file or None if error
    """
    if not results_list:
        print("No results to save.")
        return None
    
    dir_path = output_dir or OUTPUT_DIR
    file_name = filename or RESULTS_FILENAME
    output_path = os.path.join(dir_path, file_name)
    
    try:
        # Convert results to DataFrame
        results_df = pd.DataFrame(results_list)
        
        # Ensure directory exists
        os.makedirs(dir_path, exist_ok=True)
        
        # Save to CSV
        results_df.to_csv(output_path, index=False)
        print(f"Detailed WFO results saved to: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")
        return None


def save_interim_results(results_list, split_num, output_dir=None):
    """
    Save interim results after a specific split.
    
    Args:
        results_list (list): List of result dictionaries
        split_num (int): Current split number
        output_dir (str, optional): Directory to save results. Defaults to OUTPUT_DIR.
        
    Returns:
        str: Path to the saved interim file or None if error
    """
    if not results_list:
        return None
    
    # Only save periodically to avoid excessive I/O
    if split_num % 1 == 0:  # Can adjust to save less frequently
        dir_path = output_dir or OUTPUT_DIR
        interim_output_path = os.path.join(dir_path, f"interim_wfo_results.csv")
        
        try:
            interim_df = pd.DataFrame(results_list)
            interim_df.to_csv(interim_output_path, index=False)
            print(f"Saved interim results to {interim_output_path}")
            return interim_output_path
        except Exception as e:
            print(f"Error saving interim results: {e}")
    
    return None


def save_test_results(result_entry, identifier, output_dir=None):
    """
    Save individual test results for a specific symbol/timeframe combination.
    
    Args:
        result_entry (dict): The result dictionary to save
        identifier (str): Identifier for the test (e.g., "BTC-USD_1h")
        output_dir (str, optional): Directory to save results. Defaults to OUTPUT_DIR/regime_evaluation.
        
    Returns:
        str: Path to the saved file or None if error
    """
    if not result_entry:
        print("No result to save.")
        return None
    
    # Determine output directory
    dir_path = output_dir if output_dir else os.path.join(OUTPUT_DIR, "regime_evaluation")
    os.makedirs(dir_path, exist_ok=True)
    
    # Create filename with timestamp
    filename = f"regime_test_{identifier}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    output_path = os.path.join(dir_path, filename)
    
    try:
        # Convert complex nested dictionaries to strings if needed
        flattened_result = {}
        for k, v in result_entry.items():
            if isinstance(v, dict):
                flattened_result[k] = str(v)
            else:
                flattened_result[k] = v
        
        # Convert to DataFrame for easier serialization
        result_df = pd.DataFrame([flattened_result])
        
        # Save to CSV
        result_df.to_csv(output_path, index=False)
        print(f"Test results for {identifier} saved to: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error saving test results: {e}")
        return None


def create_summary_report(all_results, output_dir=None):
    """
    Create a comprehensive summary report for all regime evaluation tests.
    This is specifically for regime evaluation tests across multiple symbols/timeframes.
    
    Args:
        all_results (list): List of all test result dictionaries
        output_dir (str, optional): Directory to save report. Defaults to OUTPUT_DIR/regime_evaluation.
        
    Returns:
        str: Path to the saved report file or None if error
    """
    if not all_results:
        print("No results to summarize in regime evaluation.")
        return None
    
    # Determine output directory
    dir_path = output_dir if output_dir else os.path.join(OUTPUT_DIR, "regime_evaluation")
    os.makedirs(dir_path, exist_ok=True)
    
    # Create report filename with timestamp
    report_filename = f"regime_evaluation_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    report_path = os.path.join(dir_path, report_filename)
    
    try:
        with open(report_path, 'w') as f:
            f.write("# Regime-Aware Parameter Adaptation Evaluation Summary\n\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            # Overall summary section
            f.write("## Overall Summary\n\n")
            f.write("| Test Type | Avg Return | Avg Sharpe | Max Drawdown | Improvement |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            
            # Calculate aggregates for each test type
            avg_standard_returns = []
            avg_basic_regime_returns = []
            avg_enhanced_regime_returns = []
            
            for result in all_results:
                symbol = result.get('symbol', 'Unknown')
                timeframe = result.get('timeframe', 'Unknown')
                
                # Standard approach metrics
                std_return = result.get('standard', {}).get('avg_return', np.nan)
                if not np.isnan(std_return):
                    avg_standard_returns.append(std_return)
                
                # Basic regime metrics
                basic_return = result.get('basic_regime', {}).get('avg_return', np.nan)
                if not np.isnan(basic_return):
                    avg_basic_regime_returns.append(basic_return)
                
                # Enhanced regime metrics
                enhanced_return = result.get('enhanced_regime', {}).get('avg_return', np.nan)
                if not np.isnan(enhanced_return):
                    avg_enhanced_regime_returns.append(enhanced_return)
                
                # Add individual entry for this symbol/timeframe
                f.write(f"### {symbol} - {timeframe}\n\n")
                
                # Performance table
                f.write("| Metric | Standard | Basic Regime | Enhanced Regime | Basic Improvement | Enhanced Improvement |\n")
                f.write("| --- | --- | --- | --- | --- | --- |\n")
                
                # Add metrics rows
                std_metrics = result.get('standard', {})
                basic_metrics = result.get('basic_regime', {})
                enhanced_metrics = result.get('enhanced_regime', {})
                basic_improvement = result.get('basic_improvement', {})
                enhanced_improvement = result.get('enhanced_improvement', {})
                
                metrics = ['avg_return', 'avg_sharpe', 'max_drawdown', 'win_rate']
                metric_labels = ['Return', 'Sharpe', 'Max Drawdown', 'Win Rate']
                
                for metric, label in zip(metrics, metric_labels):
                    std_val = std_metrics.get(metric, np.nan)
                    basic_val = basic_metrics.get(metric, np.nan)
                    enhanced_val = enhanced_metrics.get(metric, np.nan)
                    basic_imp = basic_improvement.get(metric, np.nan)
                    enhanced_imp = enhanced_improvement.get(metric, np.nan)
                    
                    # Format percentages with % sign and handle NaN values
                    std_str = f"{std_val:.4f}" if not np.isnan(std_val) else "N/A"
                    basic_str = f"{basic_val:.4f}" if not np.isnan(basic_val) else "N/A"
                    enhanced_str = f"{enhanced_val:.4f}" if not np.isnan(enhanced_val) else "N/A"
                    basic_imp_str = f"{basic_imp:.2f}%" if not np.isnan(basic_imp) else "N/A"
                    enhanced_imp_str = f"{enhanced_imp:.2f}%" if not np.isnan(enhanced_imp) else "N/A"
                    
                    f.write(f"| {label} | {std_str} | {basic_str} | {enhanced_str} | {basic_imp_str} | {enhanced_imp_str} |\n")
            
            # Add overall performance summary
            f.write("\n## Average Performance Across All Tests\n\n")
            avg_std = np.mean(avg_standard_returns) if avg_standard_returns else np.nan
            avg_basic = np.mean(avg_basic_regime_returns) if avg_basic_regime_returns else np.nan
            avg_enhanced = np.mean(avg_enhanced_regime_returns) if avg_enhanced_regime_returns else np.nan
            
            # Calculate overall improvement percentages
            if not np.isnan(avg_std) and avg_std != 0:
                basic_overall_imp = 100 * (avg_basic - avg_std) / abs(avg_std) if not np.isnan(avg_basic) else np.nan
                enhanced_overall_imp = 100 * (avg_enhanced - avg_std) / abs(avg_std) if not np.isnan(avg_enhanced) else np.nan
            else:
                basic_overall_imp = np.nan
                enhanced_overall_imp = np.nan
            
            f.write("| Approach | Average Return | Improvement |\n")
            f.write("| --- | --- | --- |\n")
            f.write(f"| Standard | {avg_std:.4f} | - |\n")
            f.write(f"| Basic Regime | {avg_basic:.4f} | {basic_overall_imp:.2f}% |\n")
            f.write(f"| Enhanced Regime | {avg_enhanced:.4f} | {enhanced_overall_imp:.2f}% |\n")
            
            # Conclusion
            f.write("\n## Conclusion\n\n")
            
            if not np.isnan(enhanced_overall_imp) and enhanced_overall_imp > 0:
                f.write("The enhanced regime-aware parameter adaptation shows significant improvement ")
                f.write(f"with an average performance increase of {enhanced_overall_imp:.2f}% compared to the standard approach.\n")
            elif not np.isnan(basic_overall_imp) and basic_overall_imp > 0:
                f.write("The basic regime-aware parameter adaptation shows some improvement ")
                f.write(f"with an average performance increase of {basic_overall_imp:.2f}% compared to the standard approach.\n")
            else:
                f.write("The regime-aware parameter adaptation approaches did not show consistent improvement ")
                f.write("over the standard approach in this evaluation. Further tuning may be required.\n")
                
        print(f"Regime evaluation summary report saved to: {report_path}")
        return report_path
    
    except Exception as e:
        print(f"Error creating regime summary report: {e}")
        return None


def generate_summary_report(results_list, output_dir=None):
    """
    Generate a detailed summary report of WFO results.
    
    Args:
        results_list (list): List of result dictionaries
        output_dir (str, optional): Directory to save report. Defaults to OUTPUT_DIR/regime_evaluation.
        
    Returns:
        str: Path to the saved report file or None if error
    """
    if not results_list:
        print("No results to summarize.")
        return None
    
    # Calculate summary metrics
    valid_test_returns = [r['test_return'] for r in results_list if not np.isnan(r.get('test_return', np.nan))]
    valid_train_returns = [r['train_return'] for r in results_list if not np.isnan(r.get('train_return', np.nan))]
    robustness_ratios = [r['robustness_ratio'] for r in results_list if not np.isnan(r.get('robustness_ratio', np.nan))]
    return_stds = [r['return_std'] for r in results_list if not np.isnan(r.get('return_std', np.nan))]
    consistent_signs = [r['consistent_sign'] for r in results_list if r.get('consistent_sign', False)]
    regime_improvements = [r['regime_aware_improvement'] for r in results_list if not np.isnan(r.get('regime_aware_improvement', np.nan))]
    
    # Prepare summary statistics
    if valid_test_returns:
        avg_test_return = np.mean(valid_test_returns)
        std_test_return = np.std(valid_test_returns)
        avg_train_return = np.mean(valid_train_returns) if valid_train_returns else np.nan
        avg_robustness = np.mean(robustness_ratios) if robustness_ratios else np.nan
        avg_return_std = np.mean(return_stds) if return_stds else np.nan
        pct_consistent = 100 * len(consistent_signs) / len(results_list) if results_list else 0
        
        # Determine ratings
        if avg_robustness >= 0.7:
            robustness_rating = "Good - Strategy maintains at least 70% of training performance in testing"
        elif avg_robustness >= 0.3:
            robustness_rating = "Moderate - Strategy maintains 30-70% of training performance in testing"
        else:
            robustness_rating = "Poor - Strategy loses more than 70% of performance in testing"
            
        if avg_return_std < 0.05:
            stability_rating = "Good - Parameters perform consistently across different data segments"
        elif avg_return_std < 0.1:
            stability_rating = "Moderate - Some variation in parameter performance across segments"
        else:
            stability_rating = "Poor - Large variation in parameter performance across segments"
            
        if pct_consistent >= 75:
            consistency_rating = "Good - Parameters maintain consistent return sign in >75% of splits"
        elif pct_consistent >= 50:
            consistency_rating = "Moderate - Parameters maintain consistent return sign in 50-75% of splits"
        else:
            consistency_rating = "Poor - Parameters show inconsistent return signs across splits"
            
        # Regime improvement stats
        if regime_improvements:
            avg_regime_improvement = np.mean(regime_improvements)
            positive_improvements = [imp for imp in regime_improvements if imp > 0]
            if positive_improvements:
                pct_positive = 100 * len(positive_improvements) / len(regime_improvements)
            else:
                pct_positive = 0
        else:
            avg_regime_improvement = 0
            pct_positive = 0
    else:
        # No valid results
        return None
    
    # Create the report content
    report_content = f"""# Walk-Forward Optimization Summary Report

## Overview
- **Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Splits Analyzed:** {len(results_list)}
- **Valid Results:** {len(valid_test_returns)}/{len(results_list)}

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Train Return | {avg_train_return:.4f} |
| Average Test Return | {avg_test_return:.4f} |
| Std Dev of Test Returns | {std_test_return:.4f} |
| Average Robustness Ratio | {avg_robustness:.4f} |
| Parameter Stability (Return StdDev) | {avg_return_std:.4f} |
| Parameter Consistency | {pct_consistent:.1f}% |

## Regime Adaptation Impact

| Metric | Value |
|--------|-------|
| Avg Improvement from Regime-Aware Adaptation | {avg_regime_improvement:.4f}% |
| Percentage of Splits with Positive Improvement | {pct_positive:.1f}% |

## Quality Ratings

| Aspect | Rating |
|--------|--------|
| **Robustness** | {robustness_rating} |
| **Stability** | {stability_rating} |
| **Consistency** | {consistency_rating} |

## Recommendations

Based on the analysis:

1. **Parameter Robustness:** {
    "Consider simplifying the strategy to improve robustness" if avg_robustness < 0.5 else
    "The strategy shows good robustness between training and testing"
}

2. **Parameter Stability:** {
    "Parameters show high variability across data segments, consider more stable alternatives" if avg_return_std > 0.1 else
    "Parameter stability is acceptable"
}

3. **Regime Adaptation:** {
    "Regime-aware parameter adaptation is providing significant benefits" if avg_regime_improvement > 5 else
    "Regime-aware adaptation is providing modest benefits" if avg_regime_improvement > 0 else
    "Regime-aware adaptation is not providing benefits, consider alternative approaches"
}

4. **Next Steps:** {
    "Focus on improving parameter stability" if avg_return_std > 0.1 else
    "Focus on enhancing regime detection accuracy" if 0 < avg_regime_improvement < 5 else
    "Consider alternative strategies or market conditions" if avg_test_return < 0 else
    "Strategy is performing well, consider production testing"
}
"""
    
    # Save the report
    dir_path = output_dir or os.path.join(OUTPUT_DIR, "regime_evaluation")
    os.makedirs(dir_path, exist_ok=True)
    report_path = os.path.join(dir_path, "summary_report.md")
    
    try:
        with open(report_path, 'w') as f:
            f.write(report_content)
        print(f"Summary report saved to {report_path}")
        return report_path
    except Exception as e:
        print(f"Error saving summary report: {e}")
        return None


def print_performance_metrics(results_list):
    """
    Print key performance metrics to the console.
    
    Args:
        results_list (list): List of result dictionaries
    """
    if not results_list:
        print("No results to analyze.")
        return
    
    # Calculate summary metrics
    valid_test_returns = [r['test_return'] for r in results_list if not np.isnan(r.get('test_return', np.nan))]
    valid_train_returns = [r['train_return'] for r in results_list if not np.isnan(r.get('train_return', np.nan))]
    robustness_ratios = [r['robustness_ratio'] for r in results_list if not np.isnan(r.get('robustness_ratio', np.nan))]
    return_stds = [r['return_std'] for r in results_list if not np.isnan(r.get('return_std', np.nan))]
    consistent_signs = [r['consistent_sign'] for r in results_list if r.get('consistent_sign', False)]
    regime_improvements = [r['regime_aware_improvement'] for r in results_list if not np.isnan(r.get('regime_aware_improvement', np.nan))]
    
    if valid_test_returns:
        avg_test_return = np.mean(valid_test_returns)
        std_test_return = np.std(valid_test_returns)
        avg_train_return = np.mean(valid_train_returns) if valid_train_returns else np.nan
        avg_robustness = np.mean(robustness_ratios) if robustness_ratios else np.nan
        avg_return_std = np.mean(return_stds) if return_stds else np.nan
        pct_consistent = 100 * len(consistent_signs) / len(results_list) if results_list else 0
        
        print(f"\n--- WFO Performance Metrics ---")
        print(f"Average Train Return: {avg_train_return:.4f}")
        print(f"Average Test Return: {avg_test_return:.4f}")
        print(f"Average Robustness Ratio: {avg_robustness:.4f}")
        print(f"Average Parameter Stability (Return StdDev): {avg_return_std:.4f}")
        print(f"Percent of splits with consistent parameter performance: {pct_consistent:.1f}%")
        print(f"Std Dev of Test Returns: {std_test_return:.4f}")
        
        # Report regime adaptation improvements if available
        if regime_improvements:
            avg_regime_improvement = np.mean(regime_improvements)
            print(f"Average improvement from regime-aware adaptation: {avg_regime_improvement:.4f}%")
            positive_improvements = [imp for imp in regime_improvements if imp > 0]
            if positive_improvements:
                pct_positive = 100 * len(positive_improvements) / len(regime_improvements)
                print(f"Regime adaptation helped in {pct_positive:.1f}% of splits")
        
        # Anti-overfitting evaluation
        print("\n--- Anti-Overfitting Analysis ---")
        if avg_robustness >= 0.7:
            print("Robustness Rating: Good - Strategy maintains at least 70% of training performance in testing")
        elif avg_robustness >= 0.3:
            print("Robustness Rating: Moderate - Strategy maintains 30-70% of training performance in testing")
        else:
            print("Robustness Rating: Poor - Strategy loses more than 70% of performance in testing")
            
        if avg_return_std < 0.05:
            print("Stability Rating: Good - Parameters perform consistently across different data segments")
        elif avg_return_std < 0.1:
            print("Stability Rating: Moderate - Some variation in parameter performance across segments")
        else:
            print("Stability Rating: Poor - Large variation in parameter performance across segments")
            
        if pct_consistent >= 75:
            print("Consistency Rating: Good - Parameters maintain consistent return sign in >75% of splits")
        elif pct_consistent >= 50:
            print("Consistency Rating: Moderate - Parameters maintain consistent return sign in 50-75% of splits")
        else:
            print("Consistency Rating: Poor - Parameters show inconsistent return signs across splits")
    else:
        print("No test results were generated.")
