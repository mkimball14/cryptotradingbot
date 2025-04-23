# Cross-validation[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#cross-validation "Permanent link")


# Splitting[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#splitting "Permanent link")

Question

Learn more in [Cross-validation tutorial](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/).

To pick a fixed number of windows and optimize the window length such that they collectively cover the maximum amount of the index while keeping the train or test set non-overlapping, use [Splitter.from_n_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_n_rolling) with `length="optimize"`. Under the hood, it minimizes any empty space using SciPy.

Pick longest 20 windows for WFA such that test ranges don't overlap
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-1)splitter = vbt.Splitter.from_n_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-2) data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-3) n=20,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-4) length="optimize",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-5) split=0.7, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-6) optimize_anchor_set=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-7) set_labels=["train", "test"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-0-8))
 
[/code]

 1. 2. 


* * *

+


* * *

When using [Splitter.from_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_rolling) and the last window doesn't fit, it will be removed, leaving a gap on the right-hand side. To remove the oldest window instead, use `backwards="sorted"`.

Roll a window that fills more recent data and with no gaps between test sets
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-1)length = 1000
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-2)ratio = 0.95
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-3)train_length = round(length * ratio)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-4)test_length = length - train_length
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-6)splitter = vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-7) data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-8) length=length,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-9) split=train_length,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-10) offset_anchor_set=None,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-11) offset=-test_length,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-12) backwards="sorted"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-1-13))
 
[/code]


* * *

+


* * *

To create a gap between the train set and the test set, use [RelRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange) with `is_gap=True`.

Roll an expanding window with a variable train set, a gap of 10 rows, and a test set of 20 rows
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-1)splitter = vbt.Splitter.from_expanding(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-2) data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-3) min_length=130,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-4) offset=10, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-5) split=(1.0, vbt.RelRange(length=10, is_gap=True), 20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-6) split_range_kwargs=dict(backwards=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-2-7))
 
[/code]

 1. 2. 


* * *

+


* * *

To roll a time-periodic window, use [Splitter.from_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_ranges) with `every` and `lookback_period` arguments as date offsets.

Reserve 3 years for training and 1 year for testing
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-1)splitter = vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-2) data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-3) every="Y",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-4) lookback_period="4Y",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-5) split=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-6) vbt.RepEval("index.year != index.year[-1]"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-7) vbt.RepEval("index.year == index.year[-1]") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-8) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-3-9))
 
[/code]

 1. 2. 


# Taking[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#taking "Permanent link")

To split an object along the index (time) axis, we need to create a [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) instance and then "take" chunks from that object.

How to split an object in two lines
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-1)splitter = vbt.Splitter.from_n_rolling(data.index, n=10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-2)data_chunks = splitter.take(data) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-4)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-6)splitter = vbt.Splitter.from_ranges(df.index, every="W")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-4-7)new_df = splitter.take(df, into="reset_stacked") 
 
[/code]

 1. 2. 


* * *

+


* * *

Also, most VBT objects have a `split` method that can combine these both operations into one. The method will determine the correct splitting operation automatically based on the supplied arguments.

How to split an object in one line
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-5-1)data_chunks = data.split(n=10) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-5-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-5-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-5-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-5-5)new_df = df.vbt.split(every="W") 
 
[/code]

 1. 2. 


# Testing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#testing "Permanent link")

To cross-validate a function that takes only one parameter combination at a time on a grid of parameter combinations, use [`@vbt.cv_split`](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.cv_split). It's a combination of [`@vbt.parameterized`](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) (which takes a grid of parameter combinations and runs a function on each combination while merging the results) and [`@vbt.split`](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split) (which runs a function on each split and set combination).

Cross-validate a function to maximize the Sharpe ratio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-1)def selection(grid_results): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-2) return vbt.LabelSel([grid_results.idxmax()]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-4)@vbt.cv_split(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-5) splitter="from_n_rolling", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-6) splitter_kwargs=dict(n=10, split=0.5, set_labels=["train", "test"]), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-7) takeable_args=["data"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-8) execute_kwargs=dict(), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-9) parameterized_kwargs=dict(merge_func="concat"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-10) merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-11) selection=vbt.RepFunc(selection), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-12) return_grid=False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-13))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-14)def my_pipeline(data, param1_value, param2_value): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-15) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-16) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-18)cv_sharpe_ratios = my_pipeline( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-19) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-20) vbt.Param(param1_values),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-21) vbt.Param(param2_values)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-22))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-24)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-26)@vbt.cv_split(..., takeable_args=None) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-27)def my_pipeline(range_, data, param1_value, param2_value):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-28) data_range = data.iloc[range_]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-29) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-30) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-31)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-32)cv_sharpe_ratios = my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-33) vbt.Rep("range_"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-34) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-35) vbt.Param([1, 2, 3]),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-36) vbt.Param([1, 2, 3]),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-37) _index=data.index 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-6-38))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 


* * *

+


* * *

To skip a parameter combination, return [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.NoResult). This may be helpful to exclude a parameter combination that raises an error. `NoResult` can be also returned by the selection function to skip the entire split and set combination. Once excluded, the combination won't be visible in the final index.

Skip split and set combinations where there are no satisfactory parameters
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-3)def selection(grid_results):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-4) sharpe_ratio = grid_results.xs("Sharpe Ratio", level=-1).astype(float)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-5) return vbt.LabelSel([sharpe_ratio.idxmax()])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-7)@vbt.cv_split(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-8)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-9) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-10) stats_sr = pf.stats(agg_func=None)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-11) if stats_sr["Min Value"] > 0 and stats_sr["Total Trades"] >= 20: 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-12) return stats_sr
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-13) return vbt.NoResult
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-19)def selection(grid_results):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-20) sharpe_ratio = grid_results.xs("Sharpe Ratio", level=-1).astype(float)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-21) min_value = grid_results.xs("Min Value", level=-1).astype(float)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-22) total_trades = grid_results.xs("Total Trades", level=-1).astype(int)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-23) sharpe_ratio = sharpe_ratio[(min_value > 0) & (total_trades >= 20)]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-24) if len(sharpe_ratio) == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-25) return vbt.NoResult
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-26) return vbt.LabelSel([sharpe_ratio.idxmax()])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-28)@vbt.cv_split(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-29)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-30) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-7-31) return pf.stats(agg_func=None)
 
[/code]

 1. 2. 3. 


* * *

+


* * *

To warm up one or more indicators, instruct VBT to pass a date range instead of selecting it from data, and prepend a buffer to this date range. Then, manually select this extended date range from the data and run your indicators on the selected date range. Finally, remove the buffer from the indicator(s).

Warm up a SMA crossover
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-1)@vbt.cv_split(..., index_from="data")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-2)def buffered_sma_pipeline(data, range_, fast_period, slow_period, ...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-3) buffer_len = max(fast_period, slow_period) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-4) buffered_range = slice(range_.start - buffer_len, range_.stop) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-5) data_buffered = data.iloc[buffered_range] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-7) fast_sma_buffered = data_buffered.run("sma", fast_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-8) slow_sma_buffered = data_buffered.run("sma", slow_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-9) entries_buffered = fast_sma_buffered.real_crossed_above(slow_sma_buffered)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-10) exits_buffered = fast_sma_buffered.real_crossed_below(slow_sma_buffered)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-12) data = data_buffered.iloc[buffer_len:] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-13) entries = entries_buffered.iloc[buffer_len:]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-14) exits = exits_buffered.iloc[buffer_len:]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-15) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-17)buffered_sma_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-18) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-19) vbt.Rep("range_"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-20) vbt.Param(fast_periods, condition="x < slow_period"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-21) vbt.Param(slow_periods),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-22) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/cross-validation/#__codelineno-8-23))
 
[/code]

 1. 2. 3. 4. 5. 6.