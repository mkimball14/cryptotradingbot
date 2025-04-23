# Applications[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#applications "Permanent link")

We've got a splitter instance, what's next? 

Remember that CV involves running a backtesting job on each range. Thanks to the ability of vectorbt to process two-dimensional data, we have two major ways of accomplishing that: either 1) split all arrays into chunks, merge them into two-dimensional arrays, and run one monolithic backtesting job, or 2) run a backtesting job on each chunk separately. We can also go a hybrid path: for example, build a two-dimensional array out of each set, and backtest it in isolation from other sets. Which approach to use depends on your requirements for RAM consumption and performance: two-dimensional arrays are faster to process, but there is a threshold of the number of stacked columns after which performance starts to downgrade (mostly because your system starts using swap memory).


# Taking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#taking "Permanent link")

Taking is a process of extracting one or more "slices" from an array-like object, which is implemented by the method [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take). This method takes an object, iterates over each range in question, and takes the range from the object using [Splitter.take_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take_range) \- a dead-simple method that does `arr.iloc[range_]` on Pandas-like arrays and `arr[range_]` on NumPy arrays. Since many vectorbt classes inherit the indexing schema of Pandas, this method can even take a slice from vectorbt objects such as [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)! Once all slices have been collected, it can either stack them by rows (`stack_axis=0`) or columns (`stack_axis=1`, which is default), stack only splits and sets, or don't stack anything at all. When some slices shouldn't be stacked, they will be returned as a single Pandas Series that holds slices as values (may sound weird to have an array as a value of another array, but it's much easier for indexing than having a list).


# Without stacking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#without-stacking "Permanent link")

Let's split the close price using default arguments:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-1)>>> close_slices = splitter.take(data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-2)>>> close_slices
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-3)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-4)2018 train Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-5)2018-01-01 00:00:00+00:00 13380.0...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-6) test Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-7)2018-07-01 00:00:00+00:00 6356.81...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-8)2019 train Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-9)2019-01-01 00:00:00+00:00 3797.1...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-10) test Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-11)2019-07-01 00:00:00+00:00 10624.9...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-12)2020 train Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-13)2020-01-01 00:00:00+00:00 7200.85...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-14) test Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-15)2020-07-01 00:00:00+00:00 9232.0...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-16)2021 train Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-17)2021-01-01 00:00:00+00:00 29331.6...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-18) test Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-19)2021-07-01 00:00:00+00:00 33504.6...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-0-20)dtype: object
 
[/code]

If you're wondering what this format is: a regular Pandas Series with the split and set labels as index and the close price slices as values - basically `pd.Series` within `pd.Series` ![😛](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f61b.svg) Remember that array values can be any complex Python objects. For example, let's get the close price corresponding to the test set in 2020:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-1)>>> close_slices[2020, "test"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-3)2020-07-01 00:00:00+00:00 9232.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-4)2020-07-02 00:00:00+00:00 9086.54
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-5)2020-07-03 00:00:00+00:00 9058.26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-6) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-7)2020-12-29 00:00:00+00:00 27385.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-8)2020-12-30 00:00:00+00:00 28875.54
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-9)2020-12-31 00:00:00+00:00 28923.63
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-1-10)Freq: D, Name: Close, Length: 184, dtype: float64
 
[/code]

Bingo! 

And here's how simple is to apply a UDF on each range:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-1)>>> def get_total_return(sr):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-2)... return sr.vbt.to_returns().vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-4)>>> close_slices.apply(get_total_return) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-5)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-6)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-7) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-8)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-9) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-10)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-11) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-12)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-13) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-2-14)dtype: float64
 
[/code]

 1. 


# Complex objects[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#complex-objects "Permanent link")

One of the many unique features of vectorbt is the standardized behavior of its classes. Since this package is highly specialized on processing Pandas and NumPy arrays, most classes act as a proxy between the user and a set of such arrays; basically, each class enhances the feature set of Pandas and NumPy, and allows building connections between multiple arrays based on one common metadata stored in a [wrapper](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/#wrapping). Since such a wrapper can be sliced just like a regular Pandas array, we can slice most vectorbt objects that hold this wrapper as well, including [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter). And because we can slice them using the same indexing API as offered by Pandas arrays (thanks to [indexing](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/#indexing)), we can pass most vectorbt objects directly to [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take)!

For example, let's analyze the performance of a portfolio during different market regimes. First, we'll use the forward-looking label generator [TRENDLB](https://vectorbt.pro/pvt_7a467f6b/api/labels/generators/trendlb/#vectorbtpro.labels.generators.trendlb.TRENDLB) to annotate each data point with either 1 (uptrend), 0 (downtrend), or NaN (cannot be classified). Given the volatility of our data, we'll register an uptrend once the price jumps by 100% from its previous low point, and a downtrend once the price falls by 50% from its previous high point:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-3-1)>>> trendlb = data.run("trendlb", 1.0, 0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-3-2)>>> trendlb.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trendlb.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trendlb.dark.svg#only-dark)

Hint

If you're not sure which pair of thresholds to use, look at the plot that the labeler produces and find the thresholds that work best for you.

Then, we'll build a splitter that converts the labels into splits: 
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-4-1)>>> grouper = pd.Index(trendlb.labels.map({1: "U", 0: "D"}), name="trend")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-4-2)>>> trend_splitter = vbt.Splitter.from_grouper(data.index, grouper)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-4-3)>>> trend_splitter.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_splitter1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_splitter1.dark.svg#only-dark)

In the next step, we'll run the full grid of parameter combinations on the entire period through column stacking, and extract the returns accessor of the type [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor), which will enable us in analyzing the returns. To make a comparison, we'll also do the same on our baseline model.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-1)>>> hold_pf = vbt.Portfolio.from_holding(data)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-2)>>> hold_returns_acc = hold_pf.returns_acc
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-4)>>> fast_sma, slow_sma = vbt.talib("SMA").run_combs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-5)... data.close, np.arange(5, 50), short_names=["fast_sma", "slow_sma"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-6)>>> entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-7)>>> exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-8)>>> strat_pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-9)... data, entries, exits, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-5-10)>>> strat_returns_acc = strat_pf.returns_acc
 
[/code]

Now, take both slices from the accessor (remember that most vectorbt objects are indexable, including accessors) and plot the Sharpe heatmap for each market regime:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-6-1)>>> hold_returns_acc_slices = trend_splitter.take(hold_returns_acc)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-6-2)>>> strat_returns_acc_slices = trend_splitter.take(strat_returns_acc)
 
[/code]

UptrendsDowntrends
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-1)>>> hold_returns_acc_slices["U"].sharpe_ratio()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-2)3.4490778178230763
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-4)>>> strat_returns_acc_slices["U"].sharpe_ratio().vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-5)... x_level="fast_sma_timeperiod", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-6)... y_level="slow_sma_timeperiod",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-7)... symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-7-8)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/uptrend_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/uptrend_heatmap.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-1)>>> hold_returns_acc_slices["D"].sharpe_ratio()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-2)-1.329832516209626
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-4)>>> strat_returns_acc_slices["D"].sharpe_ratio().vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-5)... x_level="fast_sma_timeperiod", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-6)... y_level="slow_sma_timeperiod",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-7)... symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-8-8)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/downtrend_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/downtrend_heatmap.dark.svg#only-dark)

We can see that it takes a lot of effort (and some may say luck) to pick the right parameter combination and consistently beat the baseline. Since both pictures are completely different, we cannot rely on a single parameter combination; rather, we have to recognize the regime we're in and act accordingly, which is a massive challenge on its own. The above analysis should be used with caution though: there may be a position overflow from one market regime to another skewing the results since both periods are part of a single backtest. But at least we gained another bit of valuable information ![🕵](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f575.svg)

But what if we try to take slices from the portfolio? The operation would fail because each split contains gaps, and portfolio cannot be indexed with gaps, only using non-interrupting ranges. Thus, we would need to break up each split into multiple smaller splits, also called "split parts". Luckily for us, there are two functionalities that make this possible: [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range) accepts an option "by_gap" as `new_split` to split a range by gap, while [Splitter.break_up_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.break_up_splits) can apply this operation on each split. This way, we can flatten the splits such that only one trend period is processed at once. We'll also sort the splits by their start index such that they come in the same temporal order as the labels:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-9-1)>>> trend_splitter = trend_splitter.break_up_splits("by_gap", sort=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-9-2)>>> trend_splitter.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_splitter2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_splitter2.dark.svg#only-dark)

Another trick: instead of calling [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take), we can call `split` on the object directly!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-1)>>> strat_pf_slices = pf.split(trend_splitter)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-2)>>> strat_pf_slices
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-3)trend split_part
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-4)U 0 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-5)D 0 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-6)U 1 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-7)D 1 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-8)U 2 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-9)D 2 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-10)U 3 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-11)D 3 Portfolio(\n wrapper=ArrayWrapper(\n ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-10-12)dtype: object
 
[/code]

Let's analyze the median, that is, there are 50% of the parameter combinations with the same value or better, and, conversely, 50% with the same value or worse.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-1)>>> trend_range_perf = strat_pf_slices.apply(lambda pf: pf.sharpe_ratio)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-2)>>> median_trend_perf = trend_range_perf.median(axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-3)>>> median_trend_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-4)trend split_part
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-5)U 0 4.829429
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-6)D 0 -0.058159
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-7)U 1 2.874709
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-8)D 1 -0.510703
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-9)U 2 2.220633
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-10)D 2 0.917946
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-11)U 3 -0.736989
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-12)D 3 0.225841
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-11-13)dtype: float64
 
[/code]

And now visually: replace the labels in `trendlb` by the freshly-computed values.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-12-1)>>> trend_perf_ts = data.symbol_wrapper.fill().rename("trend_perf")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-12-2)>>> for label, sr in trend_splitter.bounds.iterrows():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-12-3)... trend_perf_ts.iloc[sr["start"]:sr["end"]] = median_trend_perf[label]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-12-4)>>> data.close.vbt.overlay_with_heatmap(trend_perf_ts).show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_perf.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/trend_perf.dark.svg#only-dark)

Can you spot something strange? Right, at least 50% of the parameter combinations during the last uptrend have a negative Sharpe ![🤔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f914.svg) At least my explanation is that moving averages are lagging indicators and by the time they reacted to the previous sharp decline, we already arrived at the next top; basically, the rebound took them off-guard such that any short positions from the previous decline couldn't close out on time.


# Column stacking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#column-stacking "Permanent link")

This was a glimpse into the second approach that we mentioned at the beginning of this page, which involves applying a UDF on each range separately. But how about stacking all the slices into a single one and applying our `get_total_return` just once for a nice performance boost? Turns out, we can stack the slices manually using [pandas.concat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-1)>>> close_stacked = pd.concat(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-2)... close_slices.values.tolist(), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-3)... axis=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-4)... keys=close_slices.index 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-6)>>> close_stacked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-7)split_year 2018 2019 2020 2021 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-8)set train test train test train test train test
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-9)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-10)2018-01-01 00:00:00+00:00 13380.00 NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-11)2018-01-02 00:00:00+00:00 14675.11 NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-12)2018-01-03 00:00:00+00:00 14919.51 NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-13)... ... ... ... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-14)2021-12-29 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN 46464.66
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-15)2021-12-30 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN 47120.87
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-16)2021-12-31 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN 46216.93
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-13-18)[1461 rows x 8 columns]
 
[/code]

 1. 2. 

As we can see, even though the operation produced a lot of NaNs, we now have a format that is perfectly acceptable by vectorbt. Let's apply our UDF to this array:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-1)>>> get_total_return(close_stacked)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-2)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-3)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-4) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-5)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-6) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-7)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-8) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-9)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-10) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-14-11)Name: total_return, dtype: float64
 
[/code]

Pure magic ![✨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2728.svg)

But the stacking approach above works only if we're splitting Pandas objects, but what about NumPy arrays and complex vectorbt objects? We can instruct [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take) to do the stacking job for us. The method will use [column_stack_merge](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.column_stack_merge) for stacking any array-like objects in the most efficient way. For example, let's replicate the above format using a single line of code:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-15-1)>>> close_stacked = splitter.take(data.close, into="stacked")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-15-2)>>> close_stacked.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-15-3)(1461, 8)
 
[/code]

To get rid of many NaNs in the stacked data, we can reset the index of each slice prior to stacking by adding a prefix "reset_" to any "stacked" option provided as `into`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-1)>>> close_stacked = splitter.take(data.close, into="reset_stacked")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-2)>>> close_stacked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-3)split_year 2018 2019 2020 \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-4)set train test train test train test 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-5)0 13380.00 6356.81 3797.14 10624.93 7200.85 9232.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-6)1 14675.11 6615.29 3858.56 10842.85 6965.71 9086.54 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-7)2 14919.51 6513.86 3766.78 11940.00 7344.96 9058.26 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-8).. ... ... ... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-9)181 NaN 3695.32 NaN 7388.24 9138.55 27385.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-10)182 NaN 3801.91 NaN 7246.00 NaN 28875.54 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-11)183 NaN 3702.90 NaN 7195.23 NaN 28923.63 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-13)split_year 2021 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-14)set train test 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-15)0 29331.69 33504.69 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-16)1 32178.33 33786.55 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-17)2 33000.05 34669.13 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-18).. ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-19)181 NaN 46464.66 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-20)182 NaN 47120.87 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-21)183 NaN 46216.93 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-16-23)[184 rows x 8 columns]
 
[/code]

We can also instruct the method to align each slice by the end point rather than the start point, which will push NaNs to the beginning of the array:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-1)>>> close_stacked = splitter.take(data.close, into="from_end_stacked")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-2)>>> close_stacked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-3)split_year 2018 2019 2020 \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-4)set train test train test train test 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-5)0 NaN 6356.81 NaN 10624.93 NaN 9232.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-6)1 NaN 6615.29 NaN 10842.85 NaN 9086.54 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-7)2 NaN 6513.86 NaN 11940.00 7200.85 9058.26 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-8).. ... ... ... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-9)181 5853.98 3695.32 12400.63 7388.24 9116.35 27385.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-10)182 6197.92 3801.91 11903.13 7246.00 9192.56 28875.54 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-11)183 6390.07 3702.90 10854.10 7195.23 9138.55 28923.63 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-13)split_year 2021 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-14)set train test 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-15)0 NaN 33504.69 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-16)1 NaN 33786.55 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-17)2 NaN 34669.13 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-18).. ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-19)181 34494.89 46464.66 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-20)182 35911.73 47120.87 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-21)183 35045.00 46216.93 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-17-23)[184 rows x 8 columns]
 
[/code]

Hint

If all slices have the same length, both alignments will produce the same array.

As we can see, there are two potential issues associated with this operation: the final array will have no datetime index, and the slices may have different lengths such that there will still be some NaNs present in the array. But also, we are rarely interested in stacking training and test sets together since they are bound to different pipelines, thus let's only stack the splits that belong to the same set, which will also produce slices of roughly the same length, by using "reset_stacked_splits" as `into`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-1)>>> close_stacked = splitter.take(data.close, into="reset_stacked_by_set")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-2)>>> close_stacked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-3)set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-4)train split_year 2018 2019 2020 2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-5)test split_year 2018 2019 2020 2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-18-6)dtype: object
 
[/code]

We've got some weird-looking format once again, but it's nothing more than a Series with the set labels as index and the stacked close price slices as values:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-1)>>> close_stacked["train"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-2)split_year 2018 2019 2020 2021
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-3)0 13380.00 3797.14 7200.85 29331.69
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-4)1 14675.11 3858.56 6965.71 32178.33
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-5)2 14919.51 3766.78 7344.96 33000.05
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-6).. ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-7)179 6197.92 11903.13 9116.35 35911.73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-8)180 6390.07 10854.10 9192.56 35045.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-9)181 NaN NaN 9138.55 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-19-11)[182 rows x 4 columns]
 
[/code]

By resetting the index, we save a tremendous amount of RAM: our arrays hold only `182 * 8 = 1456` instead of `1461 * 8 = 11688` (i.e., 88% less) values in memory. But how do we access the index associated with each column? We can slice it as a regular array!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-1)>>> index_slices = splitter.take(data.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-2)>>> index_slices
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-3)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-4)2018 train DatetimeIndex(['2018-01-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-5) test DatetimeIndex(['2018-07-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-6)2019 train DatetimeIndex(['2019-01-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-7) test DatetimeIndex(['2019-07-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-8)2020 train DatetimeIndex(['2020-01-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-9) test DatetimeIndex(['2020-07-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-10)2021 train DatetimeIndex(['2021-01-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-11) test DatetimeIndex(['2021-07-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-20-12)dtype: object
 
[/code]

Another way of getting the index information as by attaching the bounds to the range labels using `attach_bounds`, which can be `True` and "index" to attach the bounds in the integer and datetime format respectively. Let's use the latter but also enable `right_inclusive` to make the right bound inclusive if we want to use it in indexing with `loc`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-1)>>> close_stacked_wb = splitter.take(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-2)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-3)... into="reset_stacked_by_set",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-4)... attach_bounds="index",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-5)... right_inclusive=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-7)>>> close_stacked_wb["train"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-8)split_year 2018 2019 \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-9)start 2018-01-01 00:00:00+00:00 2019-01-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-10)end 2018-06-30 00:00:00+00:00 2019-06-30 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-11)0 13380.00 3797.14 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-12)1 14675.11 3858.56 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-13)2 14919.51 3766.78 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-14).. ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-15)179 6197.92 11903.13 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-16)180 6390.07 10854.10 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-17)181 NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-19)split_year 2020 2021 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-20)start 2020-01-01 00:00:00+00:00 2021-01-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-21)end 2020-06-30 00:00:00+00:00 2021-06-30 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-22)0 7200.85 29331.69 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-23)1 6965.71 32178.33 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-24)2 7344.96 33000.05 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-25).. ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-26)179 9116.35 35911.73 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-27)180 9192.56 35045.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-28)181 9138.55 NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-29)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-21-30)[182 rows x 4 columns]
 
[/code]

Though, to keep the index clean, we will go with the arrays without bounds first. We've established two arrays: one for training and another one for testing purposes. Let's modify our pipeline `sma_crossover_perf` from the first page to be run on a single set: replace the argument `data` with `close`, and add another argument for the frequency required by Sharpe since our index isn't datetime-like anymore.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-1)>>> @vbt.parameterized(merge_func="concat")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-2)... def set_sma_crossover_perf(close, fast_window, slow_window, freq):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-3)... fast_sma = vbt.talib("sma").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-4)... close, fast_window, short_name="fast_sma", hide_params=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-5)... slow_sma = vbt.talib("sma").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-6)... close, slow_window, short_name="slow_sma", hide_params=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-7)... entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-8)... exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-9)... pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-10)... close, entries, exits, freq=freq, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-22-11)... return pf.sharpe_ratio
 
[/code]

 1. 

Apply it on the training set to get the performance per parameter combination and split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-1)>>> train_perf = set_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-2)... close_stacked["train"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-3)... vbt.Param(np.arange(5, 50), condition="x < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-4)... vbt.Param(np.arange(5, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-5)... data.index.freq,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-6)... _execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-7)... clear_cache=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-8)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-23-10)... )
 
[/code]

Combination 990/990
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-1)>>> train_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-2)fast_window slow_window split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-3)5 6 2018 1.158471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-4) 2019 1.901410
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-5) 2020 -0.426441
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-6) 2021 0.052654
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-7) 7 2018 2.231909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-9)47 49 2021 -0.446099
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-10)48 49 2018 -1.169584
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-11) 2019 3.727154
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-12) 2020 -1.913321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-13) 2021 -0.400270
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-24-14)Name: sharpe_ratio, Length: 3960, dtype: float64
 
[/code]

A total of 990 parameter combinations were run in 20 seconds, or 20ms per run ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg)

Let's generate the performance heatmap for each split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-1)>>> train_perf.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-2)... x_level="fast_window",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-3)... y_level="slow_window",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-4)... slider_level="split_year",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-5)... symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-25-6)... ).show()
 
[/code]

 * **Dashboard**


* * *

Run the notebook to view the dashboard!

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/split_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/split_heatmap.dark.svg#only-dark)

By looking at the plot above, we can identify a number of yellow points that may be good candidates for our strategy. But, in contrast to the approach from the first page where we selected the best parameter combination, let's conduct a neighborhood analysis by finding a Sharpe ratio that's surrounded by high Sharpe ratios, so that we can diminish the effect of outliers and bring in more robustness into our optimizer.

This query can be well quantified by transforming the `train_perf` Series into a DataFrame using the accessor method [BaseAccessor.unstack_to_df](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_df) and running the accessor method [GenericAccessor.proximity_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.proximity_apply), which rolls a two-dimensional window over the entire matrix and reduces this window using a UDF. This mini-pipeline must be applied separately to each split. We will use a window of 2, that is, the two rows and columns that surround the central point, which yields a total of `(n * 2 + 1) ** 2 = 25` values. As a UDF we'll take the median, that is, each value will mean that 50% or more of the surrounding values are better than it. Our UDF will also filter out all the windows that have less than 20 valid values.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-2)... def prox_median_nb(arr): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-3)... if (~np.isnan(arr)).sum() < 20:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-4)... return np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-5)... return np.nanmedian(arr) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-7)>>> prox_perf_list = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-8)>>> for split_label, perf_sr in train_perf.groupby("split_year"): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-9)... perf_df = perf_sr.vbt.unstack_to_df(0, [1, 2]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-10)... prox_perf_df = perf_df.vbt.proximity_apply(2, prox_median_nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-11)... prox_perf_sr = prox_perf_df.stack([0, 1]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-12)... prox_perf_list.append(prox_perf_sr.reindex(perf_sr.index)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-14)>>> train_prox_perf = pd.concat(prox_perf_list) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-15)>>> train_prox_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-16)fast_window slow_window split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-17)5 6 2018 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-18) 2019 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-19) 2020 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-20) 2021 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-21) 7 2018 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-22) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-23)47 49 2021 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-24)48 49 2018 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-25) 2019 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-26) 2020 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-27) 2021 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-26-28)Length: 3960, dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 

At first, it may appear that all values are NaN, but let's prove otherwise:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-1)>>> train_prox_perf.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-2)... x_level="fast_window",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-3)... y_level="slow_window",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-4)... slider_level="split_year",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-5)... symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-27-6)... ).show()
 
[/code]

 * **Dashboard**


* * *

Run the notebook to view the dashboard!

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/split_prox_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/split_prox_heatmap.dark.svg#only-dark)

Fans of [computer vision](https://en.wikipedia.org/wiki/Computer_vision) will recognize what we did above: we used a 5x5 neighboring window acting as a [filter](https://ai.stanford.edu/~syyeung/cvweb/tutorial1.html) that replaces each pixel with the median pixel value of it and a neighborhood window of adjacent pixels. The effect is a more smooth image with sharp features removed (in our case Sharpe outliers). For example, in the first split, the highest Sharpe fell from `2.5` to `1.3`, which is still extraordinary since it means that there are points that have at least 50% of surrounding points with a Sharpe `1.3` or higher! We can now search in each split for the parameter combination that has the highest proximity performance:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-1)>>> best_params = train_prox_perf.groupby("split_year").idxmax()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-2)>>> best_params = train_prox_perf[best_params].index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-3)>>> train_prox_perf[best_params]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-4)fast_window slow_window split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-5)10 24 2018 1.311910
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-6)9 39 2019 3.801643
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-7)14 19 2020 2.077684
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-8)31 41 2021 2.142695
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-28-9)dtype: float64
 
[/code]

What we're waiting for? Let's test those combinations on our test set! But wait, how do we apply each parameter combination on each column in the test array? Isn't each parameter combination being applied on the entire input? That's right, but there's a trick: use templates to instruct the `parameterized` decorator to pass only one column at a time, depending on the parameter combination being processed.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-1)>>> test_perf = set_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-2)... vbt.RepEval(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-3)... "test_close.iloc[:, [config_idx]]", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-4)... context=dict(test_close=close_stacked["test"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-5)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-6)... vbt.Param(best_params.get_level_values("fast_window"), level=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-7)... vbt.Param(best_params.get_level_values("slow_window"), level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-8)... data.index.freq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-10)>>> test_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-11)fast_window slow_window split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-12)10 24 2018 -0.616204
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-13)9 39 2019 0.017269
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-14)14 19 2020 4.768589
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-15)31 41 2021 -0.363900
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-29-16)Name: sharpe_ratio, dtype: float64
 
[/code]

 1. 2. 

Let's compare these values against the baseline:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-1)>>> def get_index_sharpe(index):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-2)... return data.loc[index].run("from_holding").sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-4)>>> index_slices.xs("test", level="set").apply(get_index_sharpe) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-5)split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-6)2018 -1.327655
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-7)2019 -0.788038
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-8)2020 4.425057
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-9)2021 1.304871
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-30-10)dtype: float64
 
[/code]

 1. 

Not bad! Our model beats the baseline for three years in a row.


# Row stacking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#row-stacking "Permanent link")

The same way as we stacked ranges along columns, we can stack ranges along rows. The major difference between both approaches is that column stacking is meant for producing independent tests while row stacking puts ranges into the same test and thus introduces a temporal dependency between them.

What row stacking is perfect for is block resampling required for time-series bootstrapping. The bootstrap is a flexible and powerful statistical tool that can be used to quantify the uncertainty. Rather than repeatedly obtaining independent datasets (which are limited in finance), we instead obtain distinct datasets by repeatedly sampling observations from the original dataset. Each of these "bootstrap datasets" is created by sampling _with replacement_ , and is the same size as our original dataset. As a result some observations may appear more than once and some not at all (about two-thirds of the original data points appear in each bootstrap sample). Since we're working on time series, we can't simply sample the observations with replacement; rather, we should create blocks of consecutive observations, and sample those. Then we paste together sampled blocks to obtain a bootstrap dataset (learn more [here](https://asbates.rbind.io/2019/03/30/time-series-bootstrap-methods/)).

For our example, we'll use the [moving block bootstrap](https://en.wikipedia.org/wiki/Bootstrapping_\(statistics\)#Time_series:_Moving_block_bootstrap), which involves rolling a fixed-size window with an offset of just one bar:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-1)>>> block_size = int(3.15 * len(data.index) ** (1 / 3)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-2)>>> block_size
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-3)39
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-5)>>> block_splitter = vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-6)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-7)... length=block_size, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-8)... offset=1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-9)... offset_anchor="prev_start" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-11)>>> block_splitter.n_splits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-31-12)1864
 
[/code]

 1. 2. 

We've generated 1864 blocks. The next step is sampling. To generate a single sample, shuffle the blocks (i.e., splits) with replacement, which can be easily done using [Splitter.shuffle_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.shuffle_splits). We also need to limit the number of blocks such that they have roughly the same number of data points as our original data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-32-1)>>> size = int(block_splitter.n_splits / block_size)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-32-2)>>> sample_splitter = block_splitter.shuffle_splits(size=size, replace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-32-3)>>> sample_splitter.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sample_splitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sample_splitter.dark.svg#only-dark)

Let's compute the returns, "take" the slices corresponding to the blocks in the splitter, and stack them along rows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-1)>>> returns = data.returns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-2)>>> sample_rets = sample_splitter.take(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-3)... returns, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-4)... into="stacked", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-5)... stack_axis=0 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-7)>>> sample_rets
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-8)split Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-9)920 2020-02-23 00:00:00+00:00 0.029587
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-10) 2020-02-24 00:00:00+00:00 -0.028206
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-11) 2020-02-25 00:00:00+00:00 -0.035241
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-12) 2020-02-26 00:00:00+00:00 -0.056956
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-13) 2020-02-27 00:00:00+00:00 0.004321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-14) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-15)1617 2022-02-23 00:00:00+00:00 -0.025642
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-16) 2022-02-24 00:00:00+00:00 0.028918
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-17) 2022-02-25 00:00:00+00:00 0.023272
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-18) 2022-02-26 00:00:00+00:00 -0.002612
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-19) 2022-02-27 00:00:00+00:00 -0.036242
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-33-20)Name: Close, Length: 1833, dtype: float64
 
[/code]

 1. 2. 

We've created a "frankenstein" price series!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-34-1)>>> sample_rets.index = data.index[:len(sample_rets)] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-34-2)>>> sample_cumrets = data.close[0] * (sample_rets + 1).cumprod() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-34-3)>>> sample_cumrets.vbt.plot().show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/frankenstein.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/frankenstein.dark.svg#only-dark)

But one sample is not enough: we need to generate 100, 1000, or even 10000 samples for our estimates to be as accurate as possible.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-1)>>> samples_rets_list = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-2)>>> for i in vbt.ProgressBar(range(1000)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-3)... sample_spl = block_splitter.shuffle_splits(size=size, replace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-4)... sample_rets = sample_spl.take(returns, into="stacked", stack_axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-5)... sample_rets.index = returns.index[:len(sample_rets)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-6)... sample_rets.name = i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-7)... samples_rets_list.append(sample_rets)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-35-8)>>> sample_rets_stacked = pd.concat(samples_rets_list, axis=1)
 
[/code]

Sample 1000/1000

We can then analyze the distribution of a statistic of interest:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-36-1)>>> sample_sharpe = sample_rets_stacked.vbt.returns.sharpe_ratio()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-36-2)>>> sample_sharpe.vbt.boxplot(horizontal=True).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sharpe_boxplot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sharpe_boxplot.dark.svg#only-dark)

This histogram provides an estimate of the shape of the distribution of the sample Sharpe from which we can answer questions about how much the Sharpe varies across samples. Since this particular bootstrap distribution is symmetric, we can use percentile-based confidence intervals. For example, a 95% confidence interval translates to the 2.5th and 97.5th percentiles:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-37-1)>>> sample_sharpe.quantile(0.025), sample_sharpe.quantile(0.975)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-37-2)(-0.13636235254958026, 1.726050620753774)
 
[/code]

The method here can be applied to almost any other statistic or estimator, including more complex backtesting metrics.


# Applying[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#applying "Permanent link")

If the "taking" approach provides us with object slices that we can work upon, the "applying" approach using [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) runs a UDF on each range, and can not only do the "taking" part for us, but also easily merge the outputs of the UDF. First, it resolves the ranges it needs to iterate over; similarly to other methods, it takes `split_group_by` and `set_group_by` to merge ranges, but also the arguments `split` and `set_` that can be used to select specific (merged) ranges. Then, while iterating over each range, it substitutes any templates and other instructions in the positional and keyword arguments meant to be passed to the UDF. For example, by wrapping any argument with the class [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable), the method will select a slice from it and substitute the instruction with that slice. The arguments prepared in each iteration are saved in a list and passed to the executor - [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute), which you're probably already familiar with. The executor lazily executes all the iterations and (optionally) merges the outputs. _Lazily_ here means that none of the arrays will be sliced until the range is executed - good for memory ![💓](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f493.svg)

Let's run a simple example of calculating the total return of each close slice:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-1)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-2)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-3)... vbt.Takeable(data.close), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-4)... merge_func="concat" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-6)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-7)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-8) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-9)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-10) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-11)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-12) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-13)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-14) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-38-15)dtype: float64
 
[/code]

 1. 2. 

That's how easy it is! 

We could have also used templates:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-1)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-2)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-3)... vbt.RepFunc(lambda range_: data.close[range_]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-4)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-6)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-7)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-8) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-9)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-10) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-11)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-12) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-13)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-14) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-39-15)dtype: float64
 
[/code]

 1. 

Or, by manually selecting the range inside the function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-1)>>> def get_total_return(range_, data):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-2)... return data.returns[range_].vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-4)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-5)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-6)... vbt.Rep("range_"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-7)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-8)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-10)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-11)2018 train -0.534128
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-12) test -0.420523
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-13)2019 train 1.931243
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-14) test -0.337096
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-15)2020 train 0.270084
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-16) test 2.165013
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-17)2021 train 0.211639
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-18) test 0.318788
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-40-19)dtype: float64
 
[/code]

Hint

Results are slightly different because slicing returns is more accurate than slicing the price.

Taking from complex vectorbt objects works too:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-1)>>> def get_total_return(data):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-2)... return data.returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-4)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-5)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-6)... vbt.Takeable(data), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-7)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-9)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-10)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-11) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-12)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-13) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-14)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-15) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-16)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-17) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-41-18)dtype: float64
 
[/code]

 1. 

Let's run the function above on the entire split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-1)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-2)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-3)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-4)... set_group_by=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-5)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-7)split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-8)2018 -0.723251
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-9)2019 0.894908
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-10)2020 3.016697
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-11)2021 0.575665
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-42-12)dtype: float64
 
[/code]

If we need to select specific ranges to run the pipeline upon, use `split` and `set_`, which can be an integer, a label, or a sequence of such:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-1)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-2)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-3)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-4)... split=[2020, 2021],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-5)... set_="train",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-6)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-8)split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-9)2020 0.270084
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-10)2021 0.211639
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-43-11)dtype: float64
 
[/code]

Let's apply this approach to cross-validate our SMA crossover strategy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-1)>>> train_perf = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-2)... sma_crossover_perf,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-3)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-4)... vbt.Param(np.arange(5, 50), condition="x < slow_window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-5)... vbt.Param(np.arange(5, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-6)... _execute_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-7)... clear_cache=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-8)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-9)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-10)... set_="train", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-11)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-44-12)... )
 
[/code]

 1. 2. 3. 

Split 4/4
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-1)>>> train_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-2)split_year fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-3)2018 5 6 1.161661
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-4) 7 2.238117
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-5) 8 1.583246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-6) 9 1.369400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-7) 10 0.563251
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-9)2021 46 48 -0.238667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-10) 49 -0.437822
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-11) 47 48 -0.799317
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-12) 49 -0.447324
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-13) 48 49 -0.401369
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-45-14)Length: 3960, dtype: float64
 
[/code]

Let's find the best parameter combinations and pass them to the test set using templates:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-1)>>> best_params = train_perf.groupby("split_year").idxmax()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-2)>>> best_params = train_perf[best_params].index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-3)>>> train_perf[best_params]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-4)split_year fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-5)2018 6 7 2.612006
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-6)2019 35 36 4.246530
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-7)2020 16 17 2.605763
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-8)2021 32 45 3.073246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-9)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-11)>>> best_fast_windows = best_params.get_level_values("fast_window")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-12)>>> best_slow_windows = best_params.get_level_values("slow_window")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-14)>>> test_perf = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-15)... sma_crossover_perf,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-16)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-17)... vbt.RepFunc(lambda split_idx: best_fast_windows[split_idx]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-18)... vbt.RepFunc(lambda split_idx: best_slow_windows[split_idx]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-19)... set_="test",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-20)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-22)>>> test_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-23)split_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-24)2018 1.501380
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-25)2019 0.152723
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-26)2020 4.473387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-27)2021 -1.147178
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-46-28)dtype: float64
 
[/code]

 1. 

We've effectively outsourced the range iteration, taking, and execution steps.


# Iteration schemes[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#iteration-schemes "Permanent link")

The method [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) supports multiple iteration schemes. For instance, it can iterate over the selected ranges in the split-major or set-major order as a single sequence. It can also pack the splits/sets of the same set/split into the same bucket and run as a single iteration - split-wise and set-wise respectively. Why does it matter? Consider a scenario where a UDF needs to write the results to an object and then access these results in a specific order. For example, we may want a OOS range to read the results of the previous IS range, which is a requirement of parameterized CV; in such a case, the iteration can be in any order if the execution is sequential, in any major order if it (carefully) spans across multiple threads, and in the split-wise order if the execution spans across multiple processes since the sets need to share the same memory.

Split-majorSet-majorSplit-wiseSet-wise

Let's cross-validate our SMA crossover strategy using a single call! When an IS range is processed, find out the parameter combination with the highest Sharpe ratio and return it. When an OOS range is processed, access the parameter combination from the previous IS range and use it for testing. If you take a closer look at the available context at each iteration, there is no variable that holds the previous results: we need to store, write, and access the results manually. We'll iterate in a set-major order such that the splits in the training set are processed first.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-1)>>> def cv_sma_crossover(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-2)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-3)... fast_windows, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-4)... slow_windows, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-5)... split_idx, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-6)... set_idx, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-7)... train_perf_list 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-8)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-9)... if set_idx == 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-10)... train_perf = sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-11)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-12)... vbt.Param(fast_windows, condition="x < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-13)... vbt.Param(slow_windows),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-14)... _execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-15)... clear_cache=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-16)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-19)... train_perf_list.append(train_perf) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-20)... best_params = train_perf.idxmax()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-21)... return train_perf[[best_params]] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-22)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-23)... train_perf = train_perf_list[split_idx] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-24)... best_params = train_perf.idxmax()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-25)... test_perf = sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-26)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-27)... vbt.Param([best_params[0]]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-28)... vbt.Param([best_params[1]]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-30)... return test_perf 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-31)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-32)>>> train_perf_list = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-33)>>> cv_perf = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-34)... cv_sma_crossover,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-35)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-36)... np.arange(5, 50),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-37)... np.arange(5, 50),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-38)... vbt.Rep("split_idx"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-39)... vbt.Rep("set_idx"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-40)... train_perf_list,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-41)... iteration="set_major",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-42)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-47-43)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Iteration 8/8

We've got 8 iterations, one per range: the first 4 iterations correspond to the training ranges, which took the most time to execute, while the last 4 iterations correspond to the test ranges, which executed almost instantly because of just one parameter combination. Let's concatenate the training results from `train_perf_dict` and see what's inside `cv_perf`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-1)>>> train_perf = pd.concat(train_perf_list, keys=splitter.split_labels)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-2)>>> train_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-3)split_year fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-4)2018 5 6 1.161661
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-5) 7 2.238117
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-6) 8 1.583246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-7) 9 1.369400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-8) 10 0.563251
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-9) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-10)2021 46 48 -0.238667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-11) 49 -0.437822
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-12) 47 48 -0.799317
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-13) 49 -0.447324
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-14) 48 49 -0.401369
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-15)Length: 3960, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-17)>>> cv_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-18)set split_year fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-19)train 2018 6 7 2.612006
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-20) 2019 35 36 4.246530
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-21) 2020 16 17 2.605763
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-22) 2021 32 45 3.073246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-23)test 2018 6 7 1.501380
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-24) 2019 35 36 0.152723
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-25) 2020 16 17 4.473387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-26) 2021 32 45 -1.147178
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-48-27)dtype: float64
 
[/code]

Same results, awesome!


# Merging[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#merging "Permanent link")

Another great feature of this method is that it can merge arbitrary outputs: from single values and Series, to DataFrames and even tuples of such. There are two main merging options available: merging all outputs into a single object (`merge_all=True`) and merging by the main unit of iteration (`merge_all=False`). The first option does the following: it flattens all outputs into a single sequence, resolves the merging function using [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.resolve_merge_func), and calls the merging function on that sequence. If the merging function is not specified, it wraps the sequence into a Pandas Series (even if each output is a complex object). If each output is a tuple, returns multiple of such Series. Let's illustrate this by returning entries and exits, and stacking them along columns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-1)>>> def get_entries_and_exits(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-2)... fast_sma = data.run("sma", fast_window, short_name="fast_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-3)... slow_sma = data.run("sma", slow_window, short_name="slow_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-4)... entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-5)... exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-6)... return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-8)>>> entries, exits = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-9)... get_entries_and_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-10)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-11)... 20,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-12)... 30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-13)... merge_func="column_stack"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-16)>>> entries
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-17)split_year 2018 2019 2020 2021 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-18)set train test train test train test train test
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-19)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-20)2018-01-01 00:00:00+00:00 False NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-21)2018-01-02 00:00:00+00:00 False NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-22)2018-01-03 00:00:00+00:00 False NaN NaN NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-23)... ... ... ... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-24)2021-12-29 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-25)2021-12-30 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-26)2021-12-31 00:00:00+00:00 NaN NaN NaN NaN NaN NaN NaN False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-49-28)[1461 rows x 8 columns]
 
[/code]

We can then replace NaN with `False` and backtest them. If you don't want to have that many NaNs, use "reset_column_stack" as `merge_func`. We can also provide multiple merging functions (as a tuple) in case the outputs of our UDF have different formats.

Note

Even though you can return multiple different formats, the formats must remain the same across all ranges!

As said previously, we can also merge outputs by the main unit of iteration. Let's run the same UDF but only stack the masks that belong to the same split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-1)>>> entries, exits = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-2)... get_entries_and_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-3)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-4)... 50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-5)... 200,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-6)... merge_all=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-7)... merge_func="row_stack"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-10)>>> entries.loc[2018]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-11)set Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-12)train 2018-01-01 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-13) 2018-01-02 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-14) 2018-01-03 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-15) 2018-01-04 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-16) 2018-01-05 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-17) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-18)test 2018-12-27 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-19) 2018-12-28 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-20) 2018-12-29 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-21) 2018-12-30 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-22) 2018-12-31 00:00:00+00:00 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-50-23)Length: 365, dtype: bool
 
[/code]

This way, each mask covers an entire year and can be backtested as a whole. The additional level `set` provides us with the information on which set each timestamp belongs to.

In a case where a range's start and end date cannot be inferred from the merged data alone, we can instruct the method to attach this information. Let's get the total number of signals:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-1)>>> def get_signal_count(*args, **kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-2)... entries, exits = get_entries_and_exits(*args, **kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-3)... return entries.vbt.signals.total(), exits.vbt.signals.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-5)>>> entry_count, exit_count = splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-6)... get_signal_count,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-7)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-8)... 20,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-9)... 30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-10)... merge_func="concat",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-11)... attach_bounds="index" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-13)>>> entry_count
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-14)split_year set start end 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-15)2018 train 2018-01-01 00:00:00+00:00 2018-07-01 00:00:00+00:00 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-16) test 2018-07-01 00:00:00+00:00 2019-01-01 00:00:00+00:00 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-17)2019 train 2019-01-01 00:00:00+00:00 2019-07-01 00:00:00+00:00 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-18) test 2019-07-01 00:00:00+00:00 2020-01-01 00:00:00+00:00 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-19)2020 train 2020-01-01 00:00:00+00:00 2020-07-01 00:00:00+00:00 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-20) test 2020-07-01 00:00:00+00:00 2021-01-01 00:00:00+00:00 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-21)2021 train 2021-01-01 00:00:00+00:00 2021-07-01 00:00:00+00:00 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-22) test 2021-07-01 00:00:00+00:00 2022-01-01 00:00:00+00:00 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-51-23)dtype: int64
 
[/code]

 1. 

Finally, to demonstrate the power of merging functions, let's create our own merging function that plots the returned signals depending on the set!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-1)>>> def plot_entries_and_exits(results, data, keys):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-2)... set_labels = keys.get_level_values("set") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-3)... fig = data.plot(plot_volume=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-4)... train_seen = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-5)... test_seen = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-6)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-7)... for i in range(len(results)): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-8)... entries, exits = results[i] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-9)... set_label = set_labels[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-10)... if set_label == "train":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-11)... entries.vbt.signals.plot_as_entries( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-12)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-13)... trace_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-14)... marker=dict(color="limegreen"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-15)... name=f"Entries ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-16)... legendgroup=f"Entries ({set_label})", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-17)... showlegend=not train_seen 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-18)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-19)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-20)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-21)... exits.vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-22)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-23)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-24)... marker=dict(color="orange"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-25)... name=f"Exits ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-26)... legendgroup=f"Exits ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-27)... showlegend=not train_seen
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-28)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-29)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-31)... train_seen = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-32)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-33)... entries.vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-34)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-35)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-36)... marker=dict(color="skyblue"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-37)... name=f"Entries ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-38)... legendgroup=f"Entries ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-39)... showlegend=not test_seen
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-40)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-41)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-42)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-43)... exits.vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-44)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-45)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-46)... marker=dict(color="magenta"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-47)... name=f"Exits ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-48)... legendgroup=f"Entries ({set_label})",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-49)... showlegend=not test_seen
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-50)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-51)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-52)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-53)... test_seen = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-54)... return fig 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-55)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-56)>>> splitter.apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-57)... get_entries_and_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-58)... vbt.Takeable(data),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-59)... 20,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-60)... 30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-61)... merge_func=plot_entries_and_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-62)... merge_kwargs=dict(data=data, keys=vbt.Rep("keys")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-52-63)... ).show()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plot_entries_and_exits.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plot_entries_and_exits.dark.svg#only-dark)

As we can see, [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) is a flexible method that can execute any UDF on each range in the splitter. Not only it can return arrays in an analysis-friendly format, but it can also post-process and merge the outputs using another UDF, which makes it ideal for quick CV.


# Decorators[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#decorators "Permanent link")

But even the method above isn't the end of automation that vectorbt offers: similarly to the decorator [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized), which can enhance any function with a parameter processing logic, there is a decorator [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split) that can enhance just about any function with a split processing logic. The workings of this decorator are dead-simple: wrap a function, resolve a splitting specification into a splitter, and forward all arguments down to [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply). This way, we're making CV pipeline-centric and not splitter-centric. 

There are several ways how to make a function splittable:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-1)>>> @vbt.split(splitter=splitter) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-2)... def get_split_total_return(data):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-3)... return data.returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-5)>>> get_split_total_return(vbt.Takeable(data))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-6)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-7)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-8) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-9)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-10) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-11)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-12) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-13)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-14) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-15)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-17)>>> def get_total_return(data):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-18)... return data.returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-20)>>> get_split_total_return = vbt.split( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-21)... get_total_return, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-22)... splitter=splitter
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-24)>>> get_split_total_return(vbt.Takeable(data))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-25)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-26)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-27) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-28)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-29) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-30)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-31) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-32)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-33) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-53-34)dtype: float64
 
[/code]

 1. 2. 

If we didn't pass any argument to the decorator, or if we want to override some argument, we can add a prefix `_` to an argument to pass it to [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split) rather than to the function itself:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-1)>>> @vbt.split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-2)... def get_split_total_return(data):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-3)... return data.returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-5)>>> get_split_total_return(vbt.Takeable(data), _splitter=splitter)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-6)split_year set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-7)2018 train -0.522416
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-8) test -0.417491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-9)2019 train 1.858493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-10) test -0.322797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-11)2020 train 0.269093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-12) test 2.132976
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-13)2021 train 0.194783
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-14) test 0.379417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-54-15)dtype: float64
 
[/code]

A potential inconvenience of the approach above is that for each data we pass, we need to separately construct a splitter using the index of the same data. To solve this, the decorator can also take an instruction on how to create a splitter from the passed data. The instruction consists of a method name (or the actual callable) provided as `splitter`, such as "from_rolling", and keyword arguments passed to this method as `splitter_kwargs`. Let's roll a window of 30 days of the year 2020:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-1)>>> get_split_total_return(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-2)... vbt.Takeable(data.loc["2020":"2020"]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-3)... _splitter="from_rolling", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-4)... _splitter_kwargs=dict(length="30d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-6)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-7)0 0.321123
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-8)1 -0.088666
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-9)2 -0.250531
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-10)3 0.369418
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-11)4 0.093628
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-12)5 -0.059949
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-13)6 0.186424
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-14)7 0.020706
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-15)8 -0.069256
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-16)9 0.211424
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-17)10 0.372754
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-18)11 0.441005
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-55-19)dtype: float64
 
[/code]

To avoid wrapping each object to take slices from with [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable), we can also specify a list of such arguments as `takeable_args`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-1)>>> get_total_return_by_month = vbt.split(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-2)... get_total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-3)... splitter="from_grouper", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-4)... splitter_kwargs=dict(by=vbt.RepEval("index.to_period('M')")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-5)... takeable_args=["data"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-8)>>> get_total_return_by_month(data.loc["2020":"2020"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-9)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-10)2020-01 0.298859
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-11)2020-02 -0.091746
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-12)2020-03 -0.248649
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-13)2020-04 0.297622
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-14)2020-05 0.070388
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-15)2020-06 -0.104131
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-16)2020-07 0.227844
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-17)2020-08 -0.012851
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-18)2020-09 -0.096073
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-19)2020-10 0.298694
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-20)2020-11 0.431230
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-21)2020-12 0.541364
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-56-22)Freq: M, dtype: float64
 
[/code]

In the example above, a new splitter is built from every instance of data that we pass.

Furthermore, we can combine multiple decorators. For example, let's decorate the function `sma_crossover_perf` from the first page that we've already decorated with [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized), and make it split the entire period into 60% for the training set and 40% for the test set:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-1)>>> cv_sma_crossover_perf = vbt.split(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-2)... sma_crossover_perf, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-3)... splitter="from_single", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-4)... splitter_kwargs=dict(split=0.6, set_labels=["train", "test"]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-5)... takeable_args=["data"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-6)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-57-7)... )
 
[/code]

 1. 2. 

We'll run the full parameter grid on the training set only:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-1)>>> train_perf = cv_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-2)... data.loc["2020":"2021"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-3)... vbt.Param(np.arange(5, 50), condition="x < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-4)... vbt.Param(np.arange(5, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-5)... p_execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-6)... clear_cache=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-7)... collect_garbage=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-8)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-9)... _forward_kwargs_as={
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-10)... "p_execute_kwargs": "_execute_kwargs" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-11)... },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-12)... _apply_kwargs=dict(set_="train") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-58-13)... )
 
[/code]

 1. 2. 

Split 1/1
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-1)>>> train_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-2)fast_window slow_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-3)5 6 1.160003
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-4) 7 1.122994
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-5) 8 2.054193
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-6) 9 1.880043
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-7) 10 1.632951
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-9)46 48 1.362618
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-10) 49 1.415010
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-11)47 48 1.317795
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-12) 49 1.250835
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-13)48 49 0.160916
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-59-14)Length: 990, dtype: float64
 
[/code]

We can then validate the optimization performance on the test set:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-1)>>> test_perf = cv_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-2)... data.loc["2020":"2021"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-3)... train_perf.idxmax()[0],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-4)... train_perf.idxmax()[1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-5)... _apply_kwargs=dict(set_="test")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-60-6)... )
 
[/code]

Split 1/1
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-61-1)>>> test_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-61-2)1.2596407796960982
 
[/code]

Hint

If you want to have a proper Series instead of a single value returned, disable `squeeze_one_split` and `squeeze_one_set` in [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) using `_apply_kwargs`.

But even this decorator isn't the final form of automation: there's a special decorator [@cv_split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.cv_split) that combines [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split) and [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) to run the full parameter grid on the first set and the best parameter combination on the remaining sets. How is the best parameter combination defined? There's an argument `selection` that can be a template taking the previous results (available as `grid_results` in the context) and returning the integer position of the parameter combination that the user defines as the best. Moreover, the decorator can either return the best results only (`return_grid=False`), or additionally include the grid results from the training set (`return_grid=True`) or even the grid run on all sets (`return_grid="all"`).

Since we're waiting too much time for the entire grid of parameter combinations to complete, let's rewrite our pipeline with Numba to return the Sharpe ratio of a single parameter combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-1)>>> @njit(nogil=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-2)>>> def sma_crossover_perf_nb(close, fast_window, slow_window, ann_factor):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-3)... fast_sma = vbt.nb.ma_nb(close, fast_window) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-4)... slow_sma = vbt.nb.ma_nb(close, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-5)... entries = vbt.nb.crossed_above_nb(fast_sma, slow_sma) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-6)... exits = vbt.nb.crossed_above_nb(slow_sma, fast_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-7)... sim_out = vbt.pf_nb.from_signals_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-8)... target_shape=close.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-9)... group_lens=np.full(close.shape[1], 1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-10)... close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-11)... long_entries=entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-12)... short_entries=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-13)... save_returns=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-15)... return vbt.ret_nb.sharpe_ratio_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-16)... sim_out.in_outputs.returns, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-17)... ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-62-18)... )
 
[/code]

 1. 2. 3. 4. 5. 

Test the function on the full history:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-63-1)>>> sma_crossover_perf_nb(vbt.to_2d_array(data.close), 20, 30, 365)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-63-2)array([1.04969317])
 
[/code]

Note

All Numba functions that we use are expecting a two-dimensional NumPy array as input.

Finally, let's define and run CV in a parallel manner:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-1)>>> cv_sma_crossover_perf = vbt.cv_split(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-2)... sma_crossover_perf_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-3)... splitter="from_rolling",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-4)... splitter_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-5)... length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-6)... split=0.5, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-7)... set_labels=["train", "test"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-8)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-9)... takeable_args=["close"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-10)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-11)... parameterized_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-12)... engine="dask", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-13)... chunk_len="auto",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-17)>>> grid_perf, best_perf = cv_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-18)... vbt.to_2d_array(data.close),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-19)... vbt.Param(np.arange(5, 50), condition="x < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-20)... vbt.Param(np.arange(5, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-21)... pd.Timedelta(days=365) // data.index.freq, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-22)... _merge_kwargs=dict(wrapper=data.symbol_wrapper), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-23)... _index=data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-24)... _return_grid="all" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-64-25)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 7. Run the entire grid on each set. Will return both the grid results and the best results. Note that the test set will still use the previous grid, not its own.

Info

By default, the highest value is selected. To select the lowest value, set `selection="min"` in [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split). Also, make sure to change the selection template if any other merging function is being used.

Split 9/9

That was fast! ![💨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a8.svg)

Question

Why is the performance so different compared to the previous version, which, by the way, uses the same Numba functions under the hood? Remember that when running one function a thousand of times, even a 1-millisecond longer execution time translates into a 1-second longer **total** execution time.

Let's take a look at the CV results:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-1)>>> grid_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-2)split set fast_window slow_window symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-3)0 train 5 6 BTCUSDT 1.771782
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-4) 7 BTCUSDT 2.206458
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-5) 8 BTCUSDT 2.705892
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-6) 9 BTCUSDT 1.430768
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-7) 10 BTCUSDT 0.851692
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-8) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-9)8 test 46 48 BTCUSDT 0.637332
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-10) 49 BTCUSDT -0.424650
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-11) 47 48 BTCUSDT -0.214946
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-12) 49 BTCUSDT 0.231712
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-13) 48 49 BTCUSDT -0.351245
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-14)Length: 17820, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-16)>>> best_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-17)split set fast_window slow_window symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-18)0 train 19 34 BTCUSDT 4.392966
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-19) test 19 34 BTCUSDT 0.535497
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-20)1 train 6 7 BTCUSDT 2.545991
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-21) test 6 7 BTCUSDT -1.101692
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-22)2 train 18 20 BTCUSDT 4.363491
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-23) test 18 20 BTCUSDT 1.692070
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-24)3 train 14 18 BTCUSDT 3.615833
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-25) test 14 18 BTCUSDT 0.035444
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-26)4 train 18 21 BTCUSDT 3.236440
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-27) test 18 21 BTCUSDT 1.882290
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-28)5 train 20 27 BTCUSDT 3.371474
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-29) test 20 27 BTCUSDT 2.574914
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-30)6 train 11 18 BTCUSDT 4.657549
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-31) test 11 18 BTCUSDT -2.067505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-32)7 train 29 30 BTCUSDT 3.388797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-33) test 29 30 BTCUSDT 0.968127
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-34)8 train 25 28 BTCUSDT 2.149624
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-35) test 25 28 BTCUSDT 1.256857
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-65-36)dtype: float64
 
[/code]

For instance, the test results negatively correlate with the training results, meaning that the parameter combinations with the highest Sharpe tend to underperform when they overperformed previously. This actually makes sense because BTC market regimes tend to switch frequently.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-66-1)>>> best_train_perf = best_perf.xs("train", level="set")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-66-2)>>> best_test_perf = best_perf.xs("test", level="set")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-66-3)>>> best_train_perf.corr(best_test_perf)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-66-4)-0.21641517083891232
 
[/code]

To dig deeper, let's analyze the cross-set correlation of each parameter combination, that is, how the performance of a parameter combination in the training set correlates with the performance of the same parameter combination in the test set:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-67-1)>>> param_cross_set_corr = grid_perf\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-67-2)... .unstack("set")\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-67-3)... .groupby(["fast_window", "slow_window"])\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-67-4)... .apply(lambda x: x["train"].corr(x["test"]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-67-5)>>> param_cross_set_corr.vbt.heatmap(symmetric=True).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/param_cross_set_corr.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/param_cross_set_corr.dark.svg#only-dark)

Another perspective can be added by analyzing the test performance of the best parameter combinations in relation to the test performance of all parameter combinations. Let's get the relative number of parameter combinations that are better than the selected one in each split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-1)>>> grid_test_perf = grid_perf.xs("test", level="set")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-2)>>> grid_df = grid_test_perf.rename("grid").reset_index() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-3)>>> del grid_df["fast_window"] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-4)>>> del grid_df["slow_window"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-5)>>> best_df = best_test_perf.rename("best").reset_index()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-6)>>> del best_df["fast_window"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-7)>>> del best_df["slow_window"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-8)>>> merged_df = pd.merge(grid_df, best_df, on=["split", "symbol"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-9)>>> grid_better_mask = merged_df["grid"] > merged_df["best"] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-10)>>> grid_better_mask.index = grid_test_perf.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-11)>>> grid_better_cnt = grid_better_mask.groupby(["split", "symbol"]).mean() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-12)>>> grid_better_cnt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-13)split symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-14)0 BTCUSDT 0.242424
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-15)1 BTCUSDT 0.988889
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-16)2 BTCUSDT 0.214141
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-17)3 BTCUSDT 0.404040
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-18)4 BTCUSDT 0.359596
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-19)5 BTCUSDT 0.963636
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-20)6 BTCUSDT 0.908081
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-21)7 BTCUSDT 0.342424
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-22)8 BTCUSDT 0.250505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-68-23)dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 

The selected parameter combinations seam to beat the most other parameter combinations tested during the same time period, but some results are particularly disappointing: in the splits `1`, `5`, and `6`, the selected parameter combination performed worse than other 90%. 

Finally, let's compare the results against our buy-and-hold baseline. For this, we need to extract the price that belongs to each split, but how do we do that without a splitter? Believe it or not, [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split) has an argument to return the splitter without running the pipeline ![😛](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f61b.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-1)>>> cv_splitter = cv_sma_crossover_perf(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-2)... _index=data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-3)... _return_splitter=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-5)>>> stacked_close = cv_splitter.take(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-6)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-7)... into="reset_stacked",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-8)... set_="test" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-10)>>> hold_pf = vbt.Portfolio.from_holding(stacked_close, freq="daily")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-11)>>> hold_perf = hold_pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-12)>>> hold_perf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-13)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-14)0 -0.430642
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-15)1 -1.741407
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-16)2 3.408079
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-17)3 -0.556471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-18)4 0.954291
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-19)5 3.241618
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-20)6 0.686198
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-21)7 -0.038013
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-22)8 -0.917722
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-69-23)Name: sharpe_ratio, dtype: float64
 
[/code]

 1. 2. 

As we can see, the "taking" and "applying" approaches can be safely combined since the underlying splitter is guaranteed to be built in the same way and thus produce the same results (unless the splitter method has some random component and hasn't been provided with a seed).


# Modeling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#modeling "Permanent link")

The class [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) can also be helpful in cross-validating ML models. In particular, you can casually step upon a class [SplitterCV](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/sklearn_/#vectorbtpro.generic.splitting.sklearn_.SplitterCV) that acts as a regular cross-validator from scikit-learn by subclassing `BaseCrossValidator`. We'll demonstrate its usage on a simple classification problem of predicting the best entry and exit timings.

Before we start, we need to decide on features and labels that should act as predictor and response variables respectively. Features are usually multi-columnar time-series DataFrames where each row contains multiple data points (one per column) that should predict the same row in labels. Labels are usually a single-columnar time-series Series that should be predicted. Ask yourself the following questions to easily come up with a decision:

 1. _"How can the future performance be represented, preferably as a single number? Should it be the price at the next bar, the average price change over the next week, a vector of weights for rebalancing, a boolean containing a signal, or something else?"_
 2. _"What kind of data that encompasses the past performance is likely to predict the future performance? Should it be indicators, news sentiment index, past backtesting results, or something else?"_
 3. _"Which ML model can handle such a task?"_ (remember that most models are limited to just a couple of specific feature and label formats!)

For the sake of an example, we'll fit a [random forest classifier](https://en.wikipedia.org/wiki/Random_forest) on all [TA-Lib](https://github.com/mrjbq7/ta-lib) indicators stacked along columns to predict the binary labels generated by the label generator [TRENDLB](https://vectorbt.pro/pvt_7a467f6b/api/labels/generators/trendlb/#vectorbtpro.labels.generators.trendlb.TRENDLB), where 1 means an uptrend and 0 means a downtrend. Sounds like fun ![😌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f60c.svg)

First, run all the TA-Lib indicators on the entire data to get the feature set `X`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-70-1)>>> X = data.run("talib")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-70-2)>>> X.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-70-3)(1902, 174)
 
[/code]

We've got 1902 rows (dates) and 174 columns (features).

Next, generate the labels `y` (we'll use the same configuration as previously):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-71-1)>>> trendlb = data.run("trendlb", 1.0, 0.5, mode="binary")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-71-2)>>> y = trendlb.labels
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-71-3)>>> y.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-71-4)(1902,)
 
[/code]

Both the features and the labels contain NaNs, which we need to carefully take care of. If we remove the rows with at least one NaN, we'll remove all the data. Instead, we'll first remove the columns that consist entirely of NaNs or a single unique value. Also, because `X` and `y` should have the same length, we need to do the row-filtering operation on both datasets simultaneously:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-1)>>> X = X.replace([-np.inf, np.inf], np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-2)>>> invalid_column_mask = X.isnull().all(axis=0) | (X.nunique() == 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-3)>>> X = X.loc[:, ~invalid_column_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-4)>>> invalid_row_mask = X.isnull().any(axis=1) | y.isnull()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-5)>>> X = X.loc[~invalid_row_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-6)>>> y = y.loc[~invalid_row_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-7)>>> X.shape, y.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-72-8)((1773, 144), (1773,))
 
[/code]

Warning

If you worked with ML before, you'll quickly feel the danger coming from the logical operation in the first cell: we're checking for a condition across the entire column, thus potentially catching the [look-ahead bias](https://www.investopedia.com/terms/l/lookaheadbias.asp). Even though our operation isn't too dangerous because we remove only the columns that are likely to stay irrelevant in the future, other transformations such as data normalization should always be included in a [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) that's executed per split rather than once and globally.

We've successfully removed a total of 129 rows and 30 columns.

Next, we'll establish our classifier that will learn `X` to predict `y`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-73-1)>>> from sklearn.ensemble import RandomForestClassifier 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-73-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-73-3)>>> clf = RandomForestClassifier(random_state=42)
 
[/code]

 1. 

Question

Why haven't we rescaled, normalized, or reduced the dimensionality of the features? Random forests are very robust modeling techniques and can handle high noise levels as well as a high number of features.

To cross-validate the classifier, let's create an [SplitterCV](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/sklearn_/#vectorbtpro.generic.splitting.sklearn_.SplitterCV) instance that splits the entire period into expanding windows with non-overlapping test periods of 180 bars:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-1)>>> cv = vbt.SplitterCV(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-2)... "from_expanding", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-3)... min_length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-4)... offset=180, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-5)... split=-180,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-6)... set_labels=["train", "test"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-9)>>> cv_splitter = cv.get_splitter(X) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-74-10)>>> cv_splitter.plot().show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sklsplitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/sklsplitter.dark.svg#only-dark)

Finally, run the classifier on each training period and check the accuracy of its predictions on the respective test period. Even though the accuracy score is the most basic of all classification scores and has its own flaws, we'll keep things simplified for now:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-75-1)>>> from sklearn.model_selection import cross_val_score 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-75-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-75-3)>>> cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-75-4)array([1. , 0.20555556, 0.88333333, 0.72777778, 1. ,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-75-5) 0.92777778, 0.53333333, 0.30555556])
 
[/code]

 1. 

We can see that there are only two underperforming splits, and even two splits with 100% accuracy, how is this possible? Let's find out! What we need are raw predictions: we'll use the actual splitter to take the slices from `X` and `y`, generate the predictions on each test set using our classifier, and concatenate all the predictions into a single Series.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-1)>>> X_slices = cv_splitter.take(X)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-2)>>> y_slices = cv_splitter.take(y)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-4)>>> test_labels = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-5)>>> test_preds = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-6)>>> for split in X_slices.index.unique(level="split"): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-7)... X_train_slice = X_slices[(split, "train")] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-8)... y_train_slice = y_slices[(split, "train")]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-9)... X_test_slice = X_slices[(split, "test")]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-10)... y_test_slice = y_slices[(split, "test")]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-11)... slice_clf = clf.fit(X_train_slice, y_train_slice) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-12)... test_pred = slice_clf.predict(X_test_slice) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-13)... test_pred = pd.Series(test_pred, index=y_test_slice.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-14)... test_labels.append(y_test_slice)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-15)... test_preds.append(test_pred)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-17)>>> test_labels = pd.concat(test_labels).rename("labels") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-76-18)>>> test_preds = pd.concat(test_preds).rename("preds")
 
[/code]

 1. 2. 3. 4. 5. 

Let's compare the actual labels (left tab) to the predictions (right tab):

LabelsPredictions
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-77-1)>>> data.close.vbt.overlay_with_heatmap(test_labels).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/test_labels.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/test_labels.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-78-1)>>> data.close.vbt.overlay_with_heatmap(test_preds).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/test_preds.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/test_preds.dark.svg#only-dark)

The model seems to correctly classify many bigger uptrends and even issue an exit signal at the latest peak on time! Nevertheless, we shouldn't just rely on our visual intuition: let's backtest the predictions.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-2)... data.close[test_preds.index], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-3)... test_preds == 1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-4)... test_preds == 0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-5)... direction="both" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-7)>>> pf.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-8)Start 2018-05-12 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-9)End 2022-04-20 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-10)Period 1440 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-11)Start Value 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-12)Min Value 55.079685
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-13)Max Value 1238.365833
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-14)End Value 719.483655
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-15)Total Return [%] 619.483655
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-16)Benchmark Return [%] 388.524488
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-17)Total Time Exposure [%] 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-18)Max Gross Exposure [%] 532.441444
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-19)Max Drawdown [%] 71.915142
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-20)Max Drawdown Duration 244 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-21)Total Orders 20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-22)Total Fees Paid 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-23)Total Trades 20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-24)Win Rate [%] 52.631579
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-25)Best Trade [%] 511.777894
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-26)Worst Trade [%] -27.856728
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-27)Avg Winning Trade [%] 66.38609
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-28)Avg Losing Trade [%] -11.704147
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-29)Avg Winning Trade Duration 104 days 16:48:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-30)Avg Losing Trade Duration 35 days 05:20:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-31)Profit Factor 1.999834
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-32)Expectancy 32.802227
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-33)Sharpe Ratio 0.983656
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-34)Calmar Ratio 0.902507
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-35)Omega Ratio 1.202685
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-36)Sortino Ratio 1.627438
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#__codelineno-79-37)dtype: object
 
[/code]

 1. 

We've got some pretty solid statistics ![🌟](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f31f.svg)

If you're willing to accept a challenge: build a pipeline to impute and (standard-)normalize the data, [reduce the dimensionality](https://scikit-learn.org/stable/auto_examples/compose/plot_digits_pipe.html) of the features, as well as fit one of the [linear models](https://scikit-learn.org/stable/modules/linear_model.html) to predict the average price change over the next `n` bars (i.e., regression task!). Based on each prediction, you can then decide whether a position is worth opening or closing out.


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/applications/#summary "Permanent link")

Backtesting requires an overhaul of traditional cross-validation schemes centered around ML, and vectorbt offers the needed toolset. The heart of the new functionality is the juggernaut class [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter); it not only provides time-series-safe splitting schemes but also enables us to thoroughly analyze the generated splits and apply them to data of arbitrary complexity efficiently. For instance, we can enjoy the offered flexibility to either split data into slices and perform CV on them manually or construct a pipeline and let the splitter do the slicing and execution parts for us. There's even a decorator for parameterizing and cross-validating any Python function - [@cv_split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.cv_split). And for any ML-related tasks, the class [SplitterCV](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/sklearn_/#vectorbtpro.generic.splitting.sklearn_.SplitterCV) offers a splitter-enhanced interface well understood by scikit-learn and many other packages, such as by the scikit-learn compatible neural network library [skorch](https://github.com/skorch-dev/skorch) wrapping PyTorch. As a result, validation of rule-based and ML-based models has become as easy as ever ![🦋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f98b.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/cross-validation/applications.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/CrossValidation.ipynb)