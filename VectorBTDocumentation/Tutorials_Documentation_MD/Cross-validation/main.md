# Cross-validation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#cross-validation "Permanent link")

Once we develop a rule-based or ML-based strategy, it's time to backtest it. The first time around we obtain a low Sharpe ratio we're unhappy with, we decide to tweak our strategy. Eventually, after multiple iterations of tweaking parameters, we end up with a "flawless" combination of parameters and a strategy with an exceptional Sharpe ratio. However, in live trading the performance took a different turn: we essentially tanked and lost money. What went wrong?

Markets inherently have noise - small and frequent idiosyncrasies in the price data. When modelling a strategy, we want to avoid optimizing for one specific period because there is a chance the model adapts so closely to historical data that it becomes ineffective in predicting the future. It'd be like tuning a car specifically for one racetrack, while expecting it to perform well everywhere. Especially with vectorbt, which enables us to search extensive databases of historical market data for patterns, it is often possible to develop elaborate rules that appear to predict price development with close accuracy (see [_p_ -hacking](https://en.wikipedia.org/wiki/Data_dredging)) but make random guesses when applied to data outside the sample the model was constructed from.

Overfitting (aka [curve fitting](https://en.wikipedia.org/wiki/Curve_fitting)) usually occurs for one or more of the following reasons: mistaking noise for signal, and overly tweaking too many parameters. To curb overfitting, we should use [cross-validation](https://en.wikipedia.org/wiki/Cross-validation_\(statistics\)) (CV), which involves partitioning a sample of data into complementary subsets, performing the analysis on one subset of data called the training or _in-sample_ (IS) set, and validating the analysis on the other subset of data called the validation or _out-of-sample_ (OOS) set. This procedure is repeated until we have multiple OOS periods and can draw statistics from these results combined. The ultimate questions we need to ask ourselves: is our choice of parameters robust in the IS periods? Is our performance robust on the OOS periods? Because if not, we're shooting in the dark, and as a quant investor we should not leave room for second-guessing when real money is at stake.

Consider a simple strategy around a moving average crossover. 

First, we'll pull some data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-3)>>> data = vbt.BinanceData.pull("BTCUSDT", end="2022-11-01 UTC")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-4)>>> data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-5)DatetimeIndex(['2017-08-17 00:00:00+00:00', '2017-08-18 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-6) '2017-08-19 00:00:00+00:00', '2017-08-20 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-7) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-8) '2022-10-28 00:00:00+00:00', '2022-10-29 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-9) '2022-10-30 00:00:00+00:00', '2022-10-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-0-10) dtype='datetime64[ns, UTC]', name='Open time', length=1902, freq='D')
 
[/code]

Let's construct a parameterized mini-pipeline that takes data and the parameters, and returns the Sharpe ratio that should reflect the performance of our strategy on that test period:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-1)>>> @vbt.parameterized(merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-2)... def sma_crossover_perf(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-3)... fast_sma = data.run("sma", fast_window, short_name="fast_sma") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-4)... slow_sma = data.run("sma", slow_window, short_name="slow_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-5)... entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-6)... exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-7)... pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-8)... data, entries, exits, direction="both") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-1-9)... return pf.sharpe_ratio 
 
[/code]

 1. 2. 3. 4. 

Let's test a grid of `fast_window` and `slow_window` combinations on one year of that data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-1)>>> perf = sma_crossover_perf( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-2)... data["2020":"2020"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-3)... vbt.Param(np.arange(5, 50), condition="x < slow_window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-4)... vbt.Param(np.arange(5, 50)), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-5)... _execute_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-6)... clear_cache=50, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-7)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-10)>>> perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-11)fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-12)5 6 0.625318
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-13) 7 0.333243
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-14) 8 1.171861
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-15) 9 1.062940
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-16) 10 0.635302
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-17) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-18)46 48 0.534582
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-19) 49 0.573196
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-20)47 48 0.445239
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-21) 49 0.357548
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-22)48 49 -0.826995
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-2-23)Length: 990, dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 6. 

Combination 990/990

It took 30 seconds to test 990 parameter combinations, or 30 milliseconds per run. Below we're sorting the Sharpe ratios in descending order to unveil the best parameter combinations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-1)>>> perf.sort_values(ascending=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-2)fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-3)15 20 3.669815
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-4)14 19 3.484855
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-5)15 18 3.480444
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-6)14 21 3.467951
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-7)13 19 3.457093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-8) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-9)36 41 0.116606
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-10) 37 0.075805
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-11)42 43 0.004402
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-12)10 12 -0.465247
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-13)48 49 -0.826995
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-3-14)Length: 990, dtype: float64
 
[/code]

Looks like `fast_window=15` and `slow_window=20` can make us millionaires! But before we bet our entire life savings on that configuration, let's test it on the next year:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-1)>>> best_fast_window, best_slow_window = perf.idxmax() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-2)>>> sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-3)... data["2021":"2021"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-4)... best_fast_window, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-5)... best_slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-4-7)-1.1940481501019478
 
[/code]

 1. 2. 

The result is discouraging, but maybe we still performed well compared to a baseline? Let's compute the Sharpe ratio of the buy-and-hold strategy applied to that year:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-5-1)>>> data["2021":"2021"].run("from_holding").sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-5-2)0.9641311236043749
 
[/code]

 1. 

Seems like our strategy failed miserably ![🙊](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f64a.svg)

But this was just one optimization test, what if this period was an outlier and our strategy does perform well _on average_? Let's try answering this question by conducting the test above on each consecutive 180 days in the data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-1)>>> start_index = data.index[0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-2)>>> period = pd.Timedelta(days=180) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-3)>>> all_is_bounds = {} 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-4)>>> all_is_bl_perf = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-5)>>> all_is_perf = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-6)>>> all_oos_bounds = {} 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-7)>>> all_oos_bl_perf = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-8)>>> all_oos_perf = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-9)>>> split_idx = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-10)>>> period_idx = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-12)>>> with vbt.ProgressBar() as pbar: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-13)... while start_index + 2 * period <= data.index[-1]: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-14)... pbar.set_prefix(str(start_index))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-15)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-16)... is_start_index = start_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-17)... is_end_index = start_index + period - pd.Timedelta(nanoseconds=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-18)... is_data = data[is_start_index : is_end_index]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-19)... is_bl_perf = is_data.run("from_holding").sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-20)... is_perf = sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-21)... is_data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-22)... vbt.Param(np.arange(5, 50), condition="x < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-23)... vbt.Param(np.arange(5, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-24)... _execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-25)... clear_cache=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-26)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-27)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-29)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-30)... oos_start_index = start_index + period 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-31)... oos_end_index = start_index + 2 * period - pd.Timedelta(nanoseconds=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-32)... oos_data = data[oos_start_index : oos_end_index]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-33)... oos_bl_perf = oos_data.run("from_holding").sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-34)... best_fw, best_sw = is_perf.idxmax()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-35)... oos_perf = sma_crossover_perf(oos_data, best_fw, best_sw)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-36)... oos_perf_index = is_perf.index[is_perf.index == (best_fw, best_sw)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-37)... oos_perf = pd.Series([oos_perf], index=oos_perf_index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-38)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-39)... all_is_bounds[period_idx] = (is_start_index, is_end_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-40)... all_oos_bounds[period_idx + 1] = (oos_start_index, oos_end_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-41)... all_is_bl_perf[(split_idx, period_idx)] = is_bl_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-42)... all_oos_bl_perf[(split_idx, period_idx + 1)] = oos_bl_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-43)... all_is_perf[(split_idx, period_idx)] = is_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-44)... all_oos_perf[(split_idx, period_idx + 1)] = oos_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-45)... start_index = start_index + period 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-46)... split_idx += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-47)... period_idx += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-6-48)... pbar.update() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 

Period 9/9
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-1)>>> is_period_ranges = pd.DataFrame.from_dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-2)... all_is_bounds, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-3)... orient="index",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-4)... columns=["start", "end"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-6)>>> is_period_ranges.index.name = "period"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-7)>>> oos_period_ranges = pd.DataFrame.from_dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-8)... all_oos_bounds, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-9)... orient="index",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-10)... columns=["start", "end"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-12)>>> oos_period_ranges.index.name = "period"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-13)>>> period_ranges = pd.concat((is_period_ranges, oos_period_ranges)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-14)>>> period_ranges = period_ranges.drop_duplicates()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-15)>>> period_ranges
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-16) start end
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-17)period 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-18)0 2017-08-17 00:00:00+00:00 2018-02-12 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-19)1 2018-02-13 00:00:00+00:00 2018-08-11 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-20)2 2018-08-12 00:00:00+00:00 2019-02-07 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-21)3 2019-02-08 00:00:00+00:00 2019-08-06 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-22)4 2019-08-07 00:00:00+00:00 2020-02-02 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-23)5 2020-02-03 00:00:00+00:00 2020-07-31 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-24)6 2020-08-01 00:00:00+00:00 2021-01-27 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-25)7 2021-01-28 00:00:00+00:00 2021-07-26 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-26)8 2021-07-27 00:00:00+00:00 2022-01-22 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-27)9 2022-01-23 00:00:00+00:00 2022-07-21 23:59:59.999999999+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-29)>>> is_bl_perf = pd.Series(all_is_bl_perf) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-30)>>> is_bl_perf.index.names = ["split", "period"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-31)>>> oos_bl_perf = pd.Series(all_oos_bl_perf)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-32)>>> oos_bl_perf.index.names = ["split", "period"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-33)>>> bl_perf = pd.concat(( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-34)... is_bl_perf.vbt.select_levels("period"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-35)... oos_bl_perf.vbt.select_levels("period")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-36)... ))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-37)>>> bl_perf = bl_perf.drop_duplicates()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-38)>>> bl_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-39)period
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-40)0 1.846205
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-41)1 -0.430642
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-42)2 -1.741407
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-43)3 3.408079
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-44)4 -0.556471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-45)5 0.954291
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-46)6 3.241618
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-47)7 0.686198
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-48)8 -0.038013
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-49)9 -0.917722
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-50)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-51)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-52)>>> is_perf = pd.concat(all_is_perf, names=["split", "period"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-53)>>> is_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-54)split period fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-55)0 0 5 6 1.766853
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-56) 7 2.200321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-57) 8 2.698365
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-58) 9 1.426788
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-59) 10 0.849323
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-60) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-61)8 8 46 48 0.043127
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-62) 49 0.358875
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-63) 47 48 1.093769
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-64) 49 1.105751
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-65) 48 49 0.159483
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-66)Length: 8910, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-67)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-68)>>> oos_perf = pd.concat(all_oos_perf, names=["split", "period"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-69)>>> oos_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-70)split period fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-71)0 1 19 34 0.534007
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-72)1 2 6 7 -1.098628
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-73)2 3 18 20 1.687363
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-74)3 4 14 18 0.035346
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-75)4 5 18 21 1.877054
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-76)5 6 20 27 2.567751
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-77)6 7 11 18 -2.061754
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-78)7 8 29 30 0.965434
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-79)8 9 25 28 1.253361
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-80)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-81)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-82)>>> is_best_mask = is_perf.index.vbt.drop_levels("period").isin( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-83)... oos_perf.index.vbt.drop_levels("period"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-84)>>> is_best_perf = is_perf[is_best_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-85)>>> is_best_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-86)split period fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-87)0 0 19 34 4.380746
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-88)1 1 6 7 2.538909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-89)2 2 18 20 4.351354
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-90)3 3 14 18 3.605775
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-91)4 4 18 21 3.227437
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-92)5 5 20 27 3.362096
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-93)6 6 11 18 4.644594
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-94)7 7 29 30 3.379370
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-95)8 8 25 28 2.143645
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-7-96)dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 6. 

We've gathered information on 9 splits and 10 periods, it's time to evaluate the results! The index of each Series makes it almost too easy to connect information and analyze the entire thing as a whole: we can use the `split` level to connect elements that are part of the same split, the `period` level to connect elements that are part of the same time period, and `fast_window` and `slow_window` to connect elements by parameter combination. For starters, let's compare their distributions:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-1)>>> pd.concat((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-2)... is_perf.describe(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-3)... is_best_perf.describe(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-4)... is_bl_perf.describe(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-5)... oos_perf.describe(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-6)... oos_bl_perf.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-7)... ), axis=1, keys=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-8)... "IS", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-9)... "IS (Best)", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-10)... "IS (Baseline)", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-11)... "OOS (Test)", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-12)... "OOS (Baseline)"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-13)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-14) IS IS (Best) IS (Baseline) OOS (Test) OOS (Baseline)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-15)count 8882.000000 9.000000 9.000000 9.000000 9.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-16)mean 0.994383 3.514881 0.818873 0.639993 0.511770
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-17)std 1.746003 0.843435 1.746682 1.480066 1.786012
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-18)min -3.600854 2.143645 -1.741407 -2.061754 -1.741407
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-19)25% -0.272061 3.227437 -0.430642 0.035346 -0.556471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-20)50% 1.173828 3.379370 0.686198 0.965434 -0.038013
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-21)75% 2.112042 4.351354 1.846205 1.687363 0.954291
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-8-22)max 4.644594 4.644594 3.408079 2.567751 3.408079
 
[/code]

Even though the OOS results are far away from the best IS results, our strategy actually performs better (on average) than the baseline! More than 50% of periods have a Sharpe ratio of 0.96 or better, while for the baseline it's only -0.03. Another way of analyzing such information is by plotting it. Since all of those Series can be connected by period, we will use the `period` level as X-axis and the performance (Sharpe in our case) as Y-axis. Most Series can be plotted as lines, but since the IS sets capture multiple parameter combinations each, we should plot their distributions as boxes instead:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-1)>>> fig = is_perf.vbt.boxplot( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-2)... by_level="period", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-3)... trace_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-4)... line=dict(color="lightskyblue"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-5)... opacity=0.4,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-6)... showlegend=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-7)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-8)... xaxis_title="Period", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-9)... yaxis_title="Sharpe",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-11)>>> is_best_perf.vbt.select_levels("period").vbt.plot( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-12)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-13)... name="Best", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-14)... line=dict(color="limegreen", dash="dash")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-15)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-16)... fig=fig 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-18)>>> bl_perf.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-19)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-20)... name="Baseline", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-21)... line=dict(color="orange", dash="dash")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-22)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-23)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-25)>>> oos_perf.vbt.select_levels("period").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-26)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-27)... name="Test", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-28)... line=dict(color="orangered")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-29)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-30)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-31)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-9-32)>>> fig.show()
 
[/code]

 1. 2. 3. 4. 5. 6. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/example.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/example.dark.svg#only-dark)

Here's how to interpret the plot above. 

The green line follows the performance of the best parameter combination in each IS set; the fact that it touches the top-most point in each box proves that our best-parameter selection algorithm is correct. The dashed orange line follows the performance of the "buy-and-hold" strategy during each period, which acts as our baseline. The red line follows the test performance; it starts at the second range and corresponds to the parameter combination that yielded the best result during the previous period (i.e., the previous green dot).

The semi-opaque blue boxes represent the distribution of Sharpe ratios during IS (training) periods, that is, each box describes 990 parameter combinations that were tested during each period of optimization. There's no box on the far right because the last period is a OOS (test) period. For example, the period `6` (which is the seventh period because the counting starts from 0) incorporates all the Sharpe ratios ranging from `1.07` to `4.64`, which most likely means that the price had an upward trend during that time. Here's the proof:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-1)>>> is_perf_split6 = is_perf.xs(6, level="split") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-2)>>> is_perf_split6.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-3)count 990.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-4)mean 3.638821
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-5)std 0.441206
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-6)min 1.073553
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-7)25% 3.615566
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-8)50% 3.696611
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-9)75% 3.844124
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-10)max 4.644594
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-11)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-13)>>> first_left_bound = period_ranges.loc[6, "start"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-14)>>> first_right_bound = period_ranges.loc[6, "end"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-10-15)>>> data[first_left_bound : first_right_bound].plot().show() 
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/example_candlestick.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/example_candlestick.dark.svg#only-dark)

No matter which parameter combination we choose during that period of time, the Sharpe ratio will stay relatively high and will likely delude us and make our strategy appear to be performing well. To make sure that this isn't the case, we need to analyze the test performance in relation to other points, which is the main reason why we drew the lines over the [box plot](https://en.wikipedia.org/wiki/Box_plot). For instance, we can see that during the period `6` both the baseline and the test performance are located below the first quartile (or 25th percentile) - they are worse than at least 75% of the parameter combinations tested in that time range:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-1)>>> oos_perf.xs(6, level="period")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-2)split fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-3)5 20 27 2.567751
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-4)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-6)>>> is_perf_split6.quantile(0.25) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/#__codelineno-11-7)3.615566166097048
 
[/code]

 1. 

The picture gives us mixed feelings: on the one hand, the picked parameter combination does better than most parameter combinations tested during 5 different time periods; on the other hand, it even fails to beat the lowest-performing 25% of parameter combinations during other 3 time periods. In defence of our strategy, the number of splits is relatively low: most statisticians agree that the minimum sample size to get any kind of meaningful result is 100, hence the analysis above gives us just a tiny glimpse into the true performance of a SMA crossover.

So, how can we simplify all of that?

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/cross-validation/index.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/CrossValidation.ipynb)