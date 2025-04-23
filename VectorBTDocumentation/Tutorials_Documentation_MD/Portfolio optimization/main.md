# Portfolio optimization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#portfolio-optimization "Permanent link")

Portfolio optimization is all about creating a portfolio of assets such that our investment has the maximum return and minimum risk. A portfolio in this regard is the asset distribution of an investor - a weight vector, which can be well optimized for risk appetite, expected rate of return, cost minimization, and other target metrics. Moreover, such optimization can be performed on a regular basis to account for any recent changes in the market behavior.

In vectorbt, a portfolio consists of a set of asset vectors stacked into a bigger array along the column axis. By default, each of those vectors is considered as a separate backtesting instance, but we can provide a grouping instruction to treat any number of assets as a whole. Portfolio optimization is then the process of translating a set of pricing vectors (information as input) into a set of allocation vectors (actions as output), which can be fed to any simulator.

Thanks to a modular nature of vectorbt (_and to respect the holy principles of data science_), the optimization and simulation parts are being kept separately to make possible analyzing and filtering out allocation vectors even before they are actually backtested. In fact, this is quite similar to the workflow we usually apply when working with signals - 1) generate, 2) pre-analyze, 3) simulate, and 4) post-analyze. In this example, we'll discuss how to perform each of those steps for highest information yield.


# Data[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#data "Permanent link")

As always, we should start with getting some data. Since portfolio optimization involves working on a pool of assets, we need to fetch more than one symbol of data. In particular, we'll fetch one year of hourly data of 5 different cryptocurrencies:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-3)>>> data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-4)... ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-5)... start="2020-01-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-6)... end="2021-01-01 UTC",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-7)... timeframe="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-0-8)... )
 
[/code]

Symbol 5/5

Period 9/9

Let's persist the data locally to avoid re-fetching it every time we start a new runtime:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-1-1)>>> data.to_hdf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-1-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-1-3)>>> data = vbt.HDFData.pull("BinanceData.h5")
 
[/code]


# Allocation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#allocation "Permanent link")

Simply put, asset allocation is the process of deciding where to put money to work in the market - it's a horizontal vector that is consisting of weights or amount of assets and, that is located at a certain timestamp. For example, to allocate 50% to `BTCUSDT`, 20% to `ETHUSDT` and the remaining amount to other assets, the allocation vector would look like this: `[0.5, 0.2, 0.1, 0.1, 0.1]`. Very often, weight allocations sum to 1 to constantly keep the entire stake in the market, but we can also move only a part of our balance, or allocate the (continuous or discrete) number of assets as opposed to weights. Since we usually want to allocate periodically rather than invest and wait until the end of times, we also need to decide on rebalancing timestamps.


# Manually[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#manually "Permanent link")

Let's generate and simulate allocations manually to gain a better understanding of how everything fits together.


# Index points[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#index-points "Permanent link")

First thing to do is to decide at which points in time we should re-allocate. This is fairly easy using [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points), which translates a human-readable query into a list of index positions (also called "index points" or "allocation points"). Those positions are just regular indices, where `0` denotes the first row and `len(index) - 1` denotes the last one.

For example, let's translate the first day of each month into index points:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-2-1)>>> ms_points = data.wrapper.get_index_points(every="M")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-2-2)>>> ms_points
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-2-3)array([0, 744, 1434, 2177, 2895, 3639, 4356, 5100, 5844, 6564, 7308, 8027])
 
[/code]

Hint

The indices above can be validated using Pandas:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-3-1)>>> data.wrapper.index.get_indexer(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-3-2)... pd.Series(index=data.wrapper.index).resample(vbt.offset("M")).asfreq().index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-3-3)... method="bfill"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-3-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-3-5)array([0, 744, 1434, 2177, 2895, 3639, 4356, 5100, 5844, 6564, 7308, 8027])
 
[/code]

We can then translate those index points back into timestamps:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-1)>>> data.wrapper.index[ms_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-2)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-02-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-3) '2020-03-01 00:00:00+00:00', '2020-04-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-4) '2020-05-01 00:00:00+00:00', '2020-06-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-5) '2020-07-01 00:00:00+00:00', '2020-08-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-6) '2020-09-01 00:00:00+00:00', '2020-10-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-7) '2020-11-01 00:00:00+00:00', '2020-12-01 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-4-8) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

Note

[ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points) is guaranteed to return indices that can be applied on the index, unless `skipna` is disabled, which will return `-1` whenever an index point cannot be matched.

Those are our [rebalancing](https://www.investopedia.com/terms/r/rebalancing.asp) timestamps!

The main power of this method is in its flexibility: `every` can be provided as a string, an integer, `pd.Timedelta` object, or `pd.DateOffset` object:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-1)>>> example_points = data.wrapper.get_index_points(every=24 * 30) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-2)>>> data.wrapper.index[example_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-3)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-31 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-4) '2020-03-01 06:00:00+00:00', '2020-03-31 07:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-5) '2020-04-30 09:00:00+00:00', '2020-05-30 09:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-6) '2020-06-29 12:00:00+00:00', '2020-07-29 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-7) '2020-08-28 12:00:00+00:00', '2020-09-27 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-8) '2020-10-27 12:00:00+00:00', '2020-11-26 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-9) '2020-12-26 17:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-10) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-12)>>> date_offset = pd.offsets.WeekOfMonth(week=3, weekday=4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-13)>>> example_points = data.wrapper.get_index_points( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-14)... every=date_offset, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-15)... add_delta=pd.Timedelta(hours=17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-17)>>> data.wrapper.index[example_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-18)DatetimeIndex(['2020-01-24 17:00:00+00:00', '2020-02-28 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-19) '2020-03-27 17:00:00+00:00', '2020-04-24 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-20) '2020-05-22 17:00:00+00:00', '2020-06-26 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-21) '2020-07-24 17:00:00+00:00', '2020-08-28 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-22) '2020-09-25 17:00:00+00:00', '2020-10-23 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-23) '2020-11-27 17:00:00+00:00', '2020-12-25 17:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-5-24) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 

Hint

Take a look at the [available date offsets](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects).

We can also provide `start` and `end` as human-readable strings (thanks to [dateparser](https://github.com/scrapinghub/dateparser)!), integers, or `pd.Timestamp` objects, to effectively limit the entire date range:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-1)>>> example_points = data.wrapper.get_index_points(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-2)... start="April 1st 2020",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-3)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-5)>>> data.wrapper.index[example_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-6)DatetimeIndex(['2020-04-01 00:00:00+00:00', '2020-05-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-7) '2020-06-01 00:00:00+00:00', '2020-07-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-8) '2020-08-01 00:00:00+00:00', '2020-09-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-9) '2020-10-01 00:00:00+00:00', '2020-11-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-10) '2020-12-01 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-6-11) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

Another great feature is being able to provide our own dates via `on` argument and [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points) will match them with our index. If any date cannot be found, it simply uses the next date (not the previous one - we don't want to look into the future, after all):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-1)>>> example_points = data.wrapper.get_index_points(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-2)... on=["April 1st 2020 19:45", "17 September 2020 00:01"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-4)>>> data.wrapper.index[example_points]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-5)DatetimeIndex([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-6) '2020-04-01 20:00:00+00:00', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-7) '2020-09-17 01:00:00+00:00'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-7-8)], dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

But let's continue with `ms_points` generated earlier.


# Filling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#filling "Permanent link")

We've got our allocation index points, now it's time to fill actual allocations at those points. First, we need to create an empty DataFrame with symbols aligned as columns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-1)>>> symbol_wrapper = data.get_symbol_wrapper(freq="1h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-2)>>> filled_allocations = symbol_wrapper.fill() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-3)>>> filled_allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-4)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-5)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-6)2020-01-01 00:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-7)2020-01-01 01:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-8)2020-01-01 02:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-9)... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-10)2020-12-31 21:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-11)2020-12-31 22:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-12)2020-12-31 23:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-8-14)[8767 rows x 5 columns]
 
[/code]

 1. 2. 

Then, we need to generate allocations and place them at their index points. In our example, we will create allocations randomly:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-1)>>> np.random.seed(42) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-3)>>> def random_allocate_func():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-4)... weights = np.random.uniform(size=symbol_wrapper.shape[1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-5)... return weights / weights.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-7)>>> for idx in ms_points:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-8)... filled_allocations.iloc[idx] = random_allocate_func()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-10)>>> allocations = filled_allocations[~filled_allocations.isnull().any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-11)>>> allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-12)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-14)2020-01-01 00:00:00+00:00 0.133197 0.338101 0.260318 0.212900 0.055485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-15)2020-02-01 00:00:00+00:00 0.065285 0.024308 0.362501 0.251571 0.296334
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-16)2020-03-01 00:00:00+00:00 0.009284 0.437468 0.375464 0.095773 0.082010
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-17)2020-04-01 00:00:00+00:00 0.105673 0.175297 0.302353 0.248877 0.167800
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-18)2020-05-01 00:00:00+00:00 0.327909 0.074759 0.156568 0.196343 0.244421
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-19)2020-06-01 00:00:00+00:00 0.367257 0.093395 0.240527 0.277095 0.021727
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-20)2020-07-01 00:00:00+00:00 0.220313 0.061837 0.023590 0.344094 0.350166
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-21)2020-08-01 00:00:00+00:00 0.346199 0.130452 0.041828 0.293025 0.188497
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-22)2020-09-01 00:00:00+00:00 0.067065 0.272119 0.018898 0.499708 0.142210
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-23)2020-10-01 00:00:00+00:00 0.297647 0.140040 0.233647 0.245617 0.083048
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-24)2020-11-01 00:00:00+00:00 0.232128 0.185574 0.224925 0.214230 0.143143
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-9-25)2020-12-01 00:00:00+00:00 0.584609 0.056118 0.124283 0.028681 0.206309
 
[/code]

 1. 2. 

That's it - we can now use those weight vectors in simulation!


# Simulation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#simulation "Permanent link")

The simulation step is rather easy: use filled allocations as size of target percentage type, and enable a grouping with cash sharing and the dynamic call sequence.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-1)>>> pf = vbt.Portfolio.from_orders(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-2)... close=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-3)... size=filled_allocations,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-4)... size_type="targetpercent",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-5)... group_by=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-6)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-7)... call_seq="auto" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-10-8)... )
 
[/code]

 1. 2. 

We can then extract the actual allocations produced by the simulation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-1)>>> sim_alloc = pf.get_asset_value(group_by=False).vbt / pf.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-2)>>> sim_alloc 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-3)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-4)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-5)2020-01-01 00:00:00+00:00 0.133197 0.338101 0.260318 0.212900 0.055485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-6)2020-01-01 01:00:00+00:00 0.132979 0.337881 0.259649 0.214099 0.055393
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-7)2020-01-01 02:00:00+00:00 0.133259 0.337934 0.259737 0.213728 0.055342
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-8)... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-9)2020-12-31 21:00:00+00:00 0.636496 0.067686 0.188081 0.035737 0.072000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-10)2020-12-31 22:00:00+00:00 0.634586 0.068128 0.189404 0.035930 0.071952
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-11)2020-12-31 23:00:00+00:00 0.638154 0.068205 0.187649 0.035619 0.070373
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-11-13)[8766 rows x 5 columns]
 
[/code]

 1. 

We can plot the allocations either manually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-12-1)>>> sim_alloc.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-12-2)... trace_kwargs=dict(stackgroup="one"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-12-3)... use_gl=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-12-4)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/actual_allocations.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/actual_allocations.dark.svg#only-dark)

Or by using [Portfolio.plot_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.plot_allocations):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-13-1)>>> pf.plot_allocations().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/plot_allocations.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/plot_allocations.dark.svg#only-dark)

Without transaction costs such as commission and slippage, the source and target allocations should closely match at the allocation points:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-1)>>> np.isclose(allocations, sim_alloc.iloc[ms_points])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-2)array([[ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-3) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-4) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-5) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-6) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-7) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-8) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-9) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-10) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-11) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-12) [ True, True, True, True, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-14-13) [ True, True, True, True, True]])
 
[/code]


# Allocation method[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#allocation-method "Permanent link")

We've learned how to manually generate, fill, and simulate allocations. But vectorbt wouldn't be vectorbt if it hadn't a convenient function for this! And here comes [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) into play: it exposes a range of class methods to generate allocations. The workings of this class are rather simple (in contrast to its implementation): generate allocations and store them in a compressed form for further use in analysis and simulation. 

The generation part is done by the class method [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func). If you look the documentation of this method, you'll notice that it takes the same arguments as [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points) to generate index points. Then, at each of those points, it calls a user-defined allocation function `allocate_func` to get an allocation vector. Finally, all the returned vectors are concatenated into a single two-dimensional NumPy array, while index points are stored in a separate structured NumPy array of type [AllocPoints](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/records/#vectorbtpro.portfolio.pfopt.records.AllocPoints).

Let's apply the optimizer class on `random_allocate_func`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-1)>>> np.random.seed(42)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-3)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-4)... symbol_wrapper, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-5)... random_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-6)... every="M" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-15-7)... )
 
[/code]

 1. 2. 

Allocation 12/12

Hint

There is also a convenient method [PortfolioOptimizer.from_random](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_random) to generate random allocations. Try it out!

Let's take a look at the generated random allocations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-1)>>> pfo.allocations 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-2)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-3)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-4)2020-01-01 00:00:00+00:00 0.133197 0.338101 0.260318 0.212900 0.055485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-5)2020-02-01 00:00:00+00:00 0.065285 0.024308 0.362501 0.251571 0.296334
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-6)2020-03-01 00:00:00+00:00 0.009284 0.437468 0.375464 0.095773 0.082010
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-7)2020-04-01 00:00:00+00:00 0.105673 0.175297 0.302353 0.248877 0.167800
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-8)2020-05-01 00:00:00+00:00 0.327909 0.074759 0.156568 0.196343 0.244421
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-9)2020-06-01 00:00:00+00:00 0.367257 0.093395 0.240527 0.277095 0.021727
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-10)2020-07-01 00:00:00+00:00 0.220313 0.061837 0.023590 0.344094 0.350166
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-11)2020-08-01 00:00:00+00:00 0.346199 0.130452 0.041828 0.293025 0.188497
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-12)2020-09-01 00:00:00+00:00 0.067065 0.272119 0.018898 0.499708 0.142210
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-13)2020-10-01 00:00:00+00:00 0.297647 0.140040 0.233647 0.245617 0.083048
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-14)2020-11-01 00:00:00+00:00 0.232128 0.185574 0.224925 0.214230 0.143143
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-16-15)2020-12-01 00:00:00+00:00 0.584609 0.056118 0.124283 0.028681 0.206309
 
[/code]

 1. 

We can also fill the entire array to be used in simulation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-1)>>> pfo.filled_allocations 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-2)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-3)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-4)2020-01-01 00:00:00+00:00 0.133197 0.338101 0.260318 0.2129 0.055485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-5)2020-01-01 01:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-6)2020-01-01 02:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-7)2020-01-01 03:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-8)... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-9)2020-12-31 21:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-10)2020-12-31 22:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-11)2020-12-31 23:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-17-13)[8767 rows x 5 columns]
 
[/code]

 1. 

Note

A row full of NaN points means no allocation takes place at that timestamp.

Since an instance of [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) not only stores the allocation vectors but also index points themselves, we can access them under [PortfolioOptimizer.alloc_records](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.alloc_records) and analyze as regular records:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-1)>>> pfo.alloc_records.records_readable
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-2) Id Group Allocation Index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-3)0 0 group 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-4)1 1 group 2020-02-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-5)2 2 group 2020-03-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-6)3 3 group 2020-04-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-7)4 4 group 2020-05-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-8)5 5 group 2020-06-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-9)6 6 group 2020-07-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-10)7 7 group 2020-08-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-11)8 8 group 2020-09-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-12)9 9 group 2020-10-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-13)10 10 group 2020-11-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-18-14)11 11 group 2020-12-01 00:00:00+00:00
 
[/code]

The allocations can be plotted very easily using [PortfolioOptimizer.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.plot):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-19-1)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/optimizer.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/optimizer.dark.svg#only-dark)

Since [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) is a subclass of [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable), we can produce some stats describing the current optimizer state:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-1)>>> pfo.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-2)Start 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-3)End 2020-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-4)Period 365 days 06:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-5)Total Records 12
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-6)Mean Allocation: ADAUSDT 0.229714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-7)Mean Allocation: BNBUSDT 0.165789
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-8)Mean Allocation: BTCUSDT 0.197075
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-9)Mean Allocation: ETHUSDT 0.242326
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-10)Mean Allocation: XRPUSDT 0.165096
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-20-11)Name: group, dtype: object
 
[/code]

What about simulation? [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) has a special class method for this: [Portfolio.from_optimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_optimizer).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-21-1)>>> pf = vbt.Portfolio.from_optimizer(data, pfo, freq="1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-21-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-21-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-21-4)2.097991099869708
 
[/code]

Or, directly from the portfolio optimizer:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-22-1)>>> pf = pfo.simulate(data, freq="1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-22-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-22-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-22-4)2.097991099869708
 
[/code]

As we see, vectorbt yet again deploys a modular approach to make individual backtesting components as coherent as possible and as less cohesive as possible: instead of defining the entire logic inside a single backtesting module, we can split the pipeline into a set of logically separated, isolated components, each of which can be well maintained on its own.


# Once[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#once "Permanent link")

To allocate once, we can either use [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func) with `on=0`, or just use [PortfolioOptimizer.from_initial](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_initial):

from_allocate_funcfrom_initial
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-1)>>> def const_allocate_func(target_alloc):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-2)... return target_alloc
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-4)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-5)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-6)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-7)... [0.5, 0.2, 0.1, 0.1, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-8)... on=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-23-11)>>> pfo.plot().show()
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-1)>>> pfo = vbt.PortfolioOptimizer.from_initial(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-3)... [0.5, 0.2, 0.1, 0.1, 0.1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-24-6)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/once.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/once.dark.svg#only-dark)

Note

Even if the lines look straight on the chart, it doesn't mean that rebalancing takes place at each timestamp - it's mainly because vectorbt forward-fills the allocation. In reality though, the initial allocation is preserved at the first timestamp after which it usually starts to deviate. That's why it requires periodic or threshold rebalancing to preserve the allocation throughout the whole period.


# Custom array[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#custom-array "Permanent link")

If we already have an array with allocations in either compressed or filled form, we can use [PortfolioOptimizer.from_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocations) and [PortfolioOptimizer.from_filled_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_filled_allocations) respectively.

Let's create a compressed array with our own quarter allocations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-1)>>> custom_index = vbt.date_range("2020-01-01", "2021-01-01", freq="Q")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-2)>>> custom_allocations = pd.DataFrame(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-3)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-4)... [0.5, 0.2, 0.1, 0.1, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-5)... [0.1, 0.5, 0.2, 0.1, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-6)... [0.1, 0.1, 0.5, 0.2, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-7)... [0.1, 0.1, 0.1, 0.5, 0.2]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-8)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-9)... index=custom_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-10)... columns=symbol_wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-25-11)... )
 
[/code]

Whenever we pass a DataFrame, vectorbt automatically uses its index as `on` argument to place allocations at those (or next) timestamps in the original index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-1)>>> pfo = vbt.PortfolioOptimizer.from_allocations(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-3)... allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-5)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-6)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-7)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-8)2020-01-01 00:00:00+00:00 0.5 0.2 0.1 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-9)2020-04-01 00:00:00+00:00 0.1 0.5 0.2 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-10)2020-07-01 00:00:00+00:00 0.1 0.1 0.5 0.2 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-26-11)2020-10-01 00:00:00+00:00 0.1 0.1 0.1 0.5 0.2
 
[/code]

But if we passed a NumPy array, vectorbt wouldn't be able to parse the dates, and so we would need to specify the index points manually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-1)>>> pfo = vbt.PortfolioOptimizer.from_allocations(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-3)... custom_allocations.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-4)... start="2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-5)... end="2021-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-6)... every="Q"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-8)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-9)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-11)2020-01-01 00:00:00+00:00 0.5 0.2 0.1 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-12)2020-04-01 00:00:00+00:00 0.1 0.5 0.2 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-13)2020-07-01 00:00:00+00:00 0.1 0.1 0.5 0.2 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-27-14)2020-10-01 00:00:00+00:00 0.1 0.1 0.1 0.5 0.2
 
[/code]

Also, we can use allocations that have been already filled as input. In such a case, we don't even need to provide a wrapper - vectorbt will be able to parse it from the array itself (given it's a DataFrame, of course). The filled allocations are parsed by considering rows where all values are NaN as empty. Let's use the filled allocations from the previous optimizer as input to another optimizer:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-1)>>> pfo = vbt.PortfolioOptimizer.from_filled_allocations(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-2)... pfo.fill_allocations()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-4)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-5)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-6)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-7)2020-01-01 00:00:00+00:00 0.5 0.2 0.1 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-8)2020-04-01 00:00:00+00:00 0.1 0.5 0.2 0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-9)2020-07-01 00:00:00+00:00 0.1 0.1 0.5 0.2 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-28-10)2020-10-01 00:00:00+00:00 0.1 0.1 0.1 0.5 0.2
 
[/code]

Hint

You can re-run this cell any number of times - there is no information loss!


# Templates[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#templates "Permanent link")

What about more complex allocation functions, how are we supposed to pass arguments to them? One of the coolest features of vectorbt (in my personal opinion) are templates, which act as some exotic kind of callbacks. Using templates, we can instruct vectorbt to run small snippets of code at various execution points, mostly whenever new information is available.

When a new index point is processed by [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func), vectorbt substitutes all templates found in `*args` and `**kwargs` using the current context, and passes them to the allocation function. The template context consists of all arguments passed to the class method + the generated index points (`index_points`), the current iteration index (`i`), and the index point (`index_point`).

To make our example more interesting, let's allocate 100% to one asset at a time, rotationally:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-1)>>> def rotation_allocate_func(wrapper, i):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-2)... weights = np.full(len(wrapper.columns), 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-3)... weights[i % len(wrapper.columns)] = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-4)... return weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-6)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-7)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-8)... rotation_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-9)... vbt.Rep("wrapper"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-10)... vbt.Rep("i"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-11)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-29-14)>>> pfo.plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/templates.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/templates.dark.svg#only-dark)

The same can be done using evaluation templates:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-1)>>> def rotation_allocate_func(symbols, chosen_symbol):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-2)... return {s: 1 if s == chosen_symbol else 0 for s in symbols}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-4)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-5)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-6)... rotation_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-7)... vbt.RepEval("wrapper.columns"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-8)... vbt.RepEval("wrapper.columns[i % len(wrapper.columns)]"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-9)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-12)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-13)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-14)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-15)2020-01-01 00:00:00+00:00 1 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-16)2020-02-01 00:00:00+00:00 0 1 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-17)2020-03-01 00:00:00+00:00 0 0 1 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-18)2020-04-01 00:00:00+00:00 0 0 0 1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-19)2020-05-01 00:00:00+00:00 0 0 0 0 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-20)2020-06-01 00:00:00+00:00 1 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-21)2020-07-01 00:00:00+00:00 0 1 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-22)2020-08-01 00:00:00+00:00 0 0 1 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-23)2020-09-01 00:00:00+00:00 0 0 0 1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-24)2020-10-01 00:00:00+00:00 0 0 0 0 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-25)2020-11-01 00:00:00+00:00 1 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-30-26)2020-12-01 00:00:00+00:00 0 1 0 0 0
 
[/code]

 1. 

Hint

The allocation function can return a sequence of values (one per asset), a dictionary (with assets as keys), or even a Pandas Series (with assets as index), that is, anything that can be packed into a list and used as an input to a DataFrame. If some asset key hasn't been provided, its allocation will be NaN.


# Groups[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#groups "Permanent link")

Testing a single combination of parameters is boring, that's why vectorbt deploys two different parameter combination features: arguments wrapped with the class [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) and group configs. The concept of the former is similar to that you might have already discovered in [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast): wrap a sequence of multiple values with this class to combine the argument with other arguments and/or similar parameters. Let's implement constant-weighting asset allocation with different rebalancing timings:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-3)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-4)... [0.5, 0.2, 0.1, 0.1, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-5)... every=vbt.Param(["1M", "2M", "3M"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-8)>>> pf = pfo.simulate(data, freq="1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-9)>>> pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-10)every
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-11)1M 3.716574
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-12)2M 3.435540
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-13)3M 3.516401
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-31-14)Name: total_return, dtype: float64
 
[/code]

 1. 

Hint

To hide the progress bar, pass `execute_kwargs=dict(show_progress=False)`.

As we can see, vectorbt figured out that the argument `every` is a parameter, and thus it has created a column level named by the argument and placed it on top of the symbol columns. 

Let's define another parameter for weights:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-3)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-4)... vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-5)... [0.5, 0.2, 0.1, 0.1, 0.1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-6)... [0.2, 0.1, 0.1, 0.1, 0.5]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-7)... ], keys=pd.Index(["w1", "w2"], name="weights")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-8)... every=vbt.Param(["1M", "2M", "3M"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-32-9)... )
 
[/code]

 1. 

This code has generated 6 different parameter combinations (i.e., groups):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-1)>>> pfo.wrapper.grouper.get_index()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-2)MultiIndex([('1M', 'w1'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-3) ('1M', 'w2'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-4) ('2M', 'w1'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-5) ('2M', 'w2'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-6) ('3M', 'w1'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-7) ('3M', 'w2')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-33-8) names=['every', 'weights'])
 
[/code]

And applied each one on our asset columns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-1)>>> pfo.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-2)MultiIndex([('1M', 'w1', 'ADAUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-3) ('1M', 'w1', 'BNBUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-4) ('1M', 'w1', 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-6) ('3M', 'w2', 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-7) ('3M', 'w2', 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-8) ('3M', 'w2', 'XRPUSDT')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-34-9) names=['every', 'weights', 'symbol'])
 
[/code]

To select or plot the allocations corresponding to any parameter combination, we can use Pandas-like indexing **on groups** :
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-1)>>> pfo[("3M", "w2")].stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-2)Start 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-3)End 2020-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-4)Period 365 days 06:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-5)Total Records 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-6)Mean Allocation: ADAUSDT 0.2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-7)Mean Allocation: BNBUSDT 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-8)Mean Allocation: BTCUSDT 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-9)Mean Allocation: ETHUSDT 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-10)Mean Allocation: XRPUSDT 0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-35-11)Name: (3M, w2), dtype: object
 
[/code]

Note

When plotting and instead of indexing, we can provide a group name or tuple via the `column` argument.

But what about more complex groups? Representing every bit of information using parameters may be cumbersome when arguments hardly overlap. Gladly, we can use the argument `group_configs` to pass a list of dictionaries, each representing a single group and defining its arguments. Let's apply this approach to the example above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-3)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-4)... group_configs=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-5)... dict(args=([0.5, 0.2, 0.1, 0.1, 0.1],), every="1M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-6)... dict(args=([0.2, 0.1, 0.1, 0.1, 0.5],), every="2M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-7)... dict(args=([0.1, 0.1, 0.1, 0.5, 0.2],), every="3M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-8)... dict(args=([0.1, 0.1, 0.5, 0.2, 0.1],), every="1M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-9)... dict(args=([0.1, 0.5, 0.2, 0.1, 0.1],), every="2M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-10)... dict(args=([0.5, 0.2, 0.1, 0.1, 0.1],), every="3M"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-11)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-13)pfo.wrapper.grouper.get_index()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-36-14)Int64Index([0, 1, 2, 3, 4, 5], dtype='int64', name='group_config')
 
[/code]

In contrast to the previous example, where vectorbt has created two column levels corresponding to both parameters, this example produced only one where each number represents the index of a group config. Let's do something more fun: create one group that does the constant allocation and one group that does the random allocation!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-3)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-4)... group_configs=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-5)... dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-6)... allocate_func=const_allocate_func, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-7)... args=([0.5, 0.2, 0.1, 0.1, 0.1],),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-8)... _name="const" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-9)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-10)... dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-11)... allocate_func=random_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-12)... every="M",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-13)... _name="random"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-14)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-15)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-17)>>> pfo.wrapper.grouper.get_index()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-37-18)Index(['const', 'random'], dtype='object', name='group_config')
 
[/code]

 1. 

We can also combine [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) instances and group configs for the highest flexibility:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-3)... const_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-4)... group_configs={ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-5)... "const": dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-6)... allocate_func=const_allocate_func, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-7)... args=([0.5, 0.2, 0.1, 0.1, 0.1],)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-8)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-9)... "random": dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-10)... allocate_func=random_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-11)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-12)... },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-13)... every=vbt.Param(["1M", "2M", "3M"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-15)>>> pfo.wrapper.grouper.get_index()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-16)MultiIndex([('1M', 'const'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-17) ('1M', 'random'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-18) ('2M', 'const'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-19) ('2M', 'random'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-20) ('3M', 'const'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-21) ('3M', 'random')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-38-22) names=['every', 'group_config'])
 
[/code]

 1. 2. 

Info

The column levels for parameters are always placed above the column levels for group configs.


# Numba[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#numba "Permanent link")

By default, vectorbt iterates over index points using a regular Python for-loop. This has almost no impact on performance if the number of allocations is kept low, which is usually the case in portfolio optimization. This is because running the actual allocation function takes much more time compared to a single iteration of a loop. But when the number of iterations crosses tens of thousands, we might be interested in iterating using Numba.

To use Numba, enable `jitted_loop`. In this case, index points will be iterated using [allocate_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/nb/#vectorbtpro.portfolio.pfopt.nb.allocate_meta_nb), which passes the current iteration index, the current index point, and `*args`.

Note

Variable keyword arguments are not supported by Numba (yet).

Let's implement the rotational example using Numba, but now rebalancing every day:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-2)... def rotation_allocate_func_nb(i, idx, n_cols):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-3)... weights = np.full(n_cols, 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-4)... weights[i % n_cols] = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-5)... return weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-7)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-8)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-9)... rotation_allocate_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-10)... vbt.RepEval("len(wrapper.columns)"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-11)... every="D",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-12)... jitted_loop=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-15)>>> pfo.allocations.head()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-16)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-17)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-18)2020-01-05 00:00:00+00:00 1.0 0.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-19)2020-01-12 00:00:00+00:00 0.0 1.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-20)2020-01-19 00:00:00+00:00 0.0 0.0 1.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-21)2020-01-26 00:00:00+00:00 0.0 0.0 0.0 1.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-39-22)2020-02-02 00:00:00+00:00 0.0 0.0 0.0 0.0 1.0
 
[/code]


# Distribution[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#distribution "Permanent link")

If you aim for best performance, there is a possibility to run the allocation function in a distributed manner, given that each function call doesn't depend on the result of any function call before (which is only the case when you store something in a custom variable anyway).

Whenever the jitted loop is disabled, vectorbt sends all iterations to the [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) function, which is the vectorbt's in-house function execution infrastructure. This is similar to how multiple parameter combinations can be distributed when running indicators, and in fact, there is the same argument `execute_kwargs` that allows us to control the overall execution.

Let's disable the jitted loop and pass all the arguments required by our Numba-compiled function `rotation_allocate_func_nb` using templates (since the function isn't called by [allocate_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/nb/#vectorbtpro.portfolio.pfopt.nb.allocate_meta_nb) anymore!):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-3)... rotation_allocate_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-4)... vbt.Rep("i"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-5)... vbt.Rep("index_point"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-6)... vbt.RepEval("len(wrapper.columns)"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-7)... every="D",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-8)... execute_kwargs=dict(engine="dask")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-11)>>> pfo.allocations.head()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-12)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-14)2020-01-01 00:00:00+00:00 1 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-15)2020-01-02 00:00:00+00:00 0 1 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-16)2020-01-03 00:00:00+00:00 0 0 1 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-17)2020-01-04 00:00:00+00:00 0 0 0 1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-40-18)2020-01-05 00:00:00+00:00 0 0 0 0 1
 
[/code]

There is another great option for distributing the allocation process: by enabling the jitted loop with [allocate_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/nb/#vectorbtpro.portfolio.pfopt.nb.allocate_meta_nb) and chunking! This way, we can split the index points into chunks and iterate over each chunk without leaving Numba. We can control the chunking process using the `chunked` argument, which is resolved and forwarded down to [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked). We should just make sure that we provide the chunking specification for all additional arguments required by the allocation function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-3)... rotation_allocate_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-4)... vbt.RepEval("len(wrapper.columns)"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-5)... every="D",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-6)... jitted_loop=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-7)... chunked=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-8)... arg_take_spec=dict(args=vbt.ArgsTaker(None)), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-9)... engine="dask"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-12)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-14)2020-01-01 00:00:00+00:00 1.0 0.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-15)2020-01-02 00:00:00+00:00 0.0 1.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-16)2020-01-03 00:00:00+00:00 0.0 0.0 1.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-17)2020-01-04 00:00:00+00:00 0.0 0.0 0.0 1.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-41-18)2020-01-05 00:00:00+00:00 0.0 0.0 0.0 0.0 1.0
 
[/code]

 1. 

If you aren't tired of so many distribution options, here's another one: parallelize the iteration internally using Numba. This is possible by using the `jitted` argument, which is resolved and forwarded down to the `@njit` decorator of [allocate_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/nb/#vectorbtpro.portfolio.pfopt.nb.allocate_meta_nb):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-1)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-3)... rotation_allocate_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-4)... vbt.RepEval("len(wrapper.columns)"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-5)... every="D",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-6)... jitted_loop=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-7)... jitted=dict(parallel=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-10)>>> pfo.allocations.head()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-11)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-12)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-13)2020-01-01 00:00:00+00:00 1.0 0.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-14)2020-01-02 00:00:00+00:00 0.0 1.0 0.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-15)2020-01-03 00:00:00+00:00 0.0 0.0 1.0 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-16)2020-01-04 00:00:00+00:00 0.0 0.0 0.0 1.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-42-17)2020-01-05 00:00:00+00:00 0.0 0.0 0.0 0.0 1.0
 
[/code]


# Previous allocation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#previous-allocation "Permanent link")

To access the allocation generated in the previous step, we have to disable any distribution (that is, run the allocation function in a serial manner) and create a temporary list or any other container that will hold all the generated allocations. Whenever the allocation function is called, generate a new allocation and put it into that container, which can be accessed by the next allocation point. Let's slightly randomize each previous allocation to get a new one:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-1)>>> def randomize_prev_allocate_func(i, allocations, mean, std):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-2)... if i == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-3)... return allocations[0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-4)... prev_allocation = allocations[-1] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-5)... log_returns = np.random.uniform(mean, std, size=len(prev_allocation)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-6)... returns = np.exp(log_returns) - 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-7)... new_allocation = prev_allocation * (1 + returns) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-8)... new_allocation = new_allocation / new_allocation.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-9)... allocations.append(new_allocation) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-10)... return new_allocation
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-12)>>> np.random.seed(42)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-14)>>> n_symbols = len(symbol_wrapper.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-15)>>> init_allocation = np.full(n_symbols, 1 / n_symbols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-16)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-17)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-18)... randomize_prev_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-19)... i=vbt.Rep("i"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-20)... allocations=[init_allocation], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-21)... mean=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-22)... std=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-23)... every="W",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-24)... start=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-25)... exact_start=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-43-28)>>> pfo.plot().show()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/prev_allocation.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/prev_allocation.dark.svg#only-dark)


# Current allocation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#current-allocation "Permanent link")

We know how to access the previous allocation, but it has certainly changed over time, so how do we access the current (updated) allocation? We can simply forward-simulate it!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-1)>>> def current_allocate_func(price, index_point, alloc_info):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-2)... prev_alloc_info = alloc_info[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-3)... prev_index_point = prev_alloc_info["index_point"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-4)... prev_allocation = prev_alloc_info["allocation"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-5)... if prev_index_point is None:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-6)... current_allocation = prev_allocation
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-7)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-8)... prev_price_period = price.iloc[prev_index_point:index_point] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-9)... prev_pfo = vbt.PFO.from_initial(prev_price_period.vbt.wrapper, prev_allocation) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-10)... prev_pf = prev_pfo.simulate(prev_price_period)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-11)... current_allocation = prev_pf.allocations.iloc[-1] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-12)... alloc_info.append(dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-13)... index_point=index_point,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-14)... allocation=current_allocation,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-15)... ))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-16)... return current_allocation
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-18)>>> n_symbols = len(symbol_wrapper.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-19)>>> init_allocation = np.full(n_symbols, 1 / n_symbols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-20)>>> pfo = vbt.PortfolioOptimizer.from_allocate_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-21)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-22)... current_allocate_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-23)... price=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-24)... index_point=vbt.Rep("index_point"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-25)... alloc_info=[dict(index_point=None, allocation=init_allocation)], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-26)... every="W",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-27)... start=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-28)... exact_start=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-44-30)>>> pfo.plot().show()
 
[/code]

 1. 2. 3. 4. 5. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/current_allocation.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/current_allocation.dark.svg#only-dark)

The code above accesses the previous allocation, forward-simulates it, and then uses the last allocation of the simulated portfolio as the new allocation, which is identical to simulating just the very first allocation ![✨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2728.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-45-1)>>> init_pfo = vbt.PFO.from_initial(symbol_wrapper, init_allocation)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-45-2)>>> continuous_pf = pfo.simulate(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-45-3)>>> index_points = symbol_wrapper.get_index_points(every="W", start=0, exact_start=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-45-4)>>> discrete_pfo = vbt.PFO.from_allocations(symbol_wrapper, continuous_pf.allocations.iloc[index_points])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-45-5)>>> discrete_pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/current_allocation.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/current_allocation.dark.svg#only-dark)


# Optimization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#optimization "Permanent link")

Allocation periodically is fun but provides a somewhat limited machinery for what can be done. Consider a typical scenario where we want to rebalance based on a window of data rather than based on specific points in time. Using an allocation function, we would have had to additionally keep track of previous allocation or lookback period. To make things a bit easier for us, vectorbt implements an "optimization" function, which works on a range of timestamps.


# Index ranges[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#index-ranges "Permanent link")

Similar to index points, index ranges is also a collection of indices, but each element is a range of index rather than a single point. In vectorbt, index ranges are typically represented by a two-dimensional NumPy array where the first column holds range start indices (including) and the second column holds range end indices (excluding). And similarly to how we translated human-readable queries into an array with indices using [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points), we can translate similar queries into index ranges using [ArrayWrapper.get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges).

Let's demonstrate usage of this method by splitting the entire period into month ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-1)>>> example_ranges = data.wrapper.get_index_ranges(every="M")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-2)>>> example_ranges[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-3)array([0, 744, 1434, 2177, 2895, 3639, 4356, 5100, 5844, 6564, 7308])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-5)>>> example_ranges[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-46-6)array([744, 1434, 2177, 2895, 3639, 4356, 5100, 5844, 6564, 7308, 8027])
 
[/code]

What happened is the following: vectorbt created a new datetime index with a monthly frequency, and created a range from each pair of values in that index. 

To translate each index range back into timestamps:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-1)>>> data.wrapper.index[example_ranges[0][0]:example_ranges[1][0]] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-2)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-01 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-3) '2020-01-01 02:00:00+00:00', '2020-01-01 03:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-4) '2020-01-01 04:00:00+00:00', '2020-01-01 05:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-6) '2020-01-31 18:00:00+00:00', '2020-01-31 19:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-7) '2020-01-31 20:00:00+00:00', '2020-01-31 21:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-8) '2020-01-31 22:00:00+00:00', '2020-01-31 23:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-47-9) dtype='datetime64[ns, UTC]', name='Open time', length=744, freq=None)
 
[/code]

 1. 

Important

The right bound (second column) is always excluding, thus you shouldn't use it for indexing because it can point to an element that exceeds the length of the index.

We see that the first range covers values from `2020-01-01` to `2020-01-31` \- a month in time.

In cases where we want to look back for a pre-determined period of time rather than up to the previous allocation timestamp, we can use the `lookback_period` argument. Below, we are generating new indices each month while looking back for 3 months:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-1)>>> example_ranges = data.wrapper.get_index_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-2)... every="M", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-3)... lookback_period="3M" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-6)>>> def get_index_bounds(range_starts, range_ends): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-7)... for i in range(len(range_starts)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-8)... start_idx = range_starts[i] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-9)... end_idx = range_ends[i] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-10)... range_index = data.wrapper.index[start_idx:end_idx]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-11)... yield range_index[0], range_index[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-13)>>> list(get_index_bounds(*example_ranges))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-14)[(Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-15) Timestamp('2020-03-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-16) (Timestamp('2020-02-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-17) Timestamp('2020-04-30 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-18) (Timestamp('2020-03-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-19) Timestamp('2020-05-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-20) (Timestamp('2020-04-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-21) Timestamp('2020-06-30 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-22) (Timestamp('2020-05-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-23) Timestamp('2020-07-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-24) (Timestamp('2020-06-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-25) Timestamp('2020-08-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-26) (Timestamp('2020-07-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-27) Timestamp('2020-09-30 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-28) (Timestamp('2020-08-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-29) Timestamp('2020-10-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-30) (Timestamp('2020-09-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-48-31) Timestamp('2020-11-30 23:00:00+0000', tz='UTC'))]
 
[/code]

 1. 2. 3. 4. 

But what if we know exactly at which date each range should start and/or end? In contrast to index points, the `start` and `end` arguments can be collections of indices or timestamps denoting the range bounds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-1)>>> example_ranges = data.wrapper.get_index_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-2)... start=["2020-01-01", "2020-04-01", "2020-08-01"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-3)... end=["2020-04-01", "2020-08-01", "2020-12-01"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-6)>>> list(get_index_bounds(*example_ranges))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-7)[(Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-8) Timestamp('2020-03-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-9) (Timestamp('2020-04-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-10) Timestamp('2020-07-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-11) (Timestamp('2020-08-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-49-12) Timestamp('2020-11-30 23:00:00+0000', tz='UTC'))]
 
[/code]

Hint

We can mark the first timestamp as excluding and the last timestamp as including by setting `closed_start` to False and `closed_end` to True respectively. Note that these conditions are applied on the input, while the output is still following the schema _from including to excluding_.

In addition, if `start` or `end` is a single value, it will automatically broadcast to match the length of another argument. Let's simulate the movement of an expanding window:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-1)>>> example_ranges = data.wrapper.get_index_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-2)... start="2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-3)... end=["2020-04-01", "2020-08-01", "2020-12-01"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-6)>>> list(get_index_bounds(*example_ranges))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-7)[(Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-8) Timestamp('2020-03-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-9) (Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-10) Timestamp('2020-07-31 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-11) (Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-50-12) Timestamp('2020-11-30 23:00:00+0000', tz='UTC'))]
 
[/code]

Another argument worth mentioning is `fixed_start`, which combined with `every` can also simulate an expanding window:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-1)>>> example_ranges = data.wrapper.get_index_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-2)... every="Q",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-3)... exact_start=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-4)... fixed_start=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-7)>>> list(get_index_bounds(*example_ranges))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-8)[(Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-9) Timestamp('2020-03-30 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-10) (Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-11) Timestamp('2020-06-29 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-12) (Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-13) Timestamp('2020-09-29 23:00:00+0000', tz='UTC')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-14) (Timestamp('2020-01-01 00:00:00+0000', tz='UTC'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-51-15) Timestamp('2020-12-30 23:00:00+0000', tz='UTC'))]
 
[/code]

 1. 


# Optimization method[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#optimization-method "Permanent link")

Just like [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func), which is applied on index points, there a class method [PortfolioOptimizer.from_optimize_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_optimize_func), which is applied on index ranges. The workings of this method are almost identical to its counterpart, except that each iteration calls an optimization function `optimize_func` that is concerned with an index range (available as `index_slice` via the template context), and all index ranges are stored as records of type [AllocRanges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/records/#vectorbtpro.portfolio.pfopt.records.AllocRanges), which is a subclass of [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges).

Let's do something simple: allocate inversely proportional to the return of an asset. This will allocate more to assets that have been performing poorly in an expectation that we will buy them at a discounted price and they will turn bullish in the upcoming time period.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-1)>>> def inv_rank_optimize_func(price, index_slice):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-2)... price_period = price.iloc[index_slice] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-3)... first_price = price_period.iloc[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-4)... last_price = price_period.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-5)... ret = (last_price - first_price) / first_price 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-6)... ranks = ret.rank(ascending=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-7)... return ranks / ranks.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-9)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-10)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-11)... inv_rank_optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-12)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-13)... vbt.Rep("index_slice"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-14)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-17)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-18)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-19)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-20)2020-02-01 00:00:00+00:00 0.066667 0.200000 0.266667 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-21)2020-03-01 00:00:00+00:00 0.333333 0.133333 0.266667 0.066667 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-22)2020-04-01 00:00:00+00:00 0.266667 0.200000 0.133333 0.333333 0.066667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-23)2020-05-01 00:00:00+00:00 0.066667 0.200000 0.266667 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-24)2020-06-01 00:00:00+00:00 0.066667 0.266667 0.200000 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-25)2020-07-01 00:00:00+00:00 0.066667 0.266667 0.200000 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-26)2020-08-01 00:00:00+00:00 0.066667 0.266667 0.333333 0.133333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-27)2020-09-01 00:00:00+00:00 0.333333 0.133333 0.266667 0.066667 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-28)2020-10-01 00:00:00+00:00 0.266667 0.066667 0.133333 0.333333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-29)2020-11-01 00:00:00+00:00 0.333333 0.266667 0.066667 0.133333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-52-30)2020-12-01 00:00:00+00:00 0.133333 0.333333 0.266667 0.200000 0.066667
 
[/code]

 1. 2. 3. 4. 5. 

To select the index range from an array automatically, we can wrap the array with [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-1)>>> def inv_rank_optimize_func(price):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-2)... first_price = price.iloc[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-3)... last_price = price.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-4)... ret = (last_price - first_price) / first_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-5)... ranks = ret.rank(ascending=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-6)... return ranks / ranks.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-8)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-9)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-10)... inv_rank_optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-11)... vbt.Takeable(data.get("Close")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-12)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-53-13)... )
 
[/code]

Hint

Although this approach introduces a tiny overhead, it has a key advantage over the manual approach: VBT knows how to select an index range even if the takeable array is a Pandas object with an index or frequency different from that of the optimization. This is possible thanks to VBT's robust resampling.

To validate the allocation array, we first need to access the index ranges that our portfolio optimization was performed upon, which are stored under the same attribute as index points - [PortfolioOptimizer.alloc_records](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.alloc_records):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-1)>>> pfo.alloc_records.records_readable
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-2) Range Id Group Start Index End Index \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-3)0 0 group 2020-01-01 00:00:00+00:00 2020-02-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-4)1 1 group 2020-02-01 00:00:00+00:00 2020-03-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-5)2 2 group 2020-03-01 00:00:00+00:00 2020-04-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-6)3 3 group 2020-04-01 00:00:00+00:00 2020-05-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-7)4 4 group 2020-05-01 00:00:00+00:00 2020-06-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-8)5 5 group 2020-06-01 00:00:00+00:00 2020-07-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-9)6 6 group 2020-07-01 00:00:00+00:00 2020-08-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-10)7 7 group 2020-08-01 00:00:00+00:00 2020-09-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-11)8 8 group 2020-09-01 00:00:00+00:00 2020-10-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-12)9 9 group 2020-10-01 00:00:00+00:00 2020-11-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-13)10 10 group 2020-11-01 00:00:00+00:00 2020-12-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-15) Allocation Index Status 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-16)0 2020-02-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-17)1 2020-03-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-18)2 2020-04-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-19)3 2020-05-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-20)4 2020-06-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-21)5 2020-07-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-22)6 2020-08-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-23)7 2020-09-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-24)8 2020-10-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-25)9 2020-11-01 00:00:00+00:00 Closed 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-54-26)10 2020-12-01 00:00:00+00:00 Closed 
 
[/code]

We see three different types of timestamps: a start (`start_idx`), an end (`end_idx`), and an allocation timestamp (`alloc_idx`). The start and end ones contain our index ranges, while the allocation ones contain the timestamps were the allocations were actually placed. By default, vectorbt places an allocation at the end of each index range. In cases where the end index exceeds the bounds (remember that it's an excluded index), the status of the range is marked as "Open", otherwise as "Closed" (which means we can safely use that allocation). Allocation and filled allocation arrays contain only closed allocations.

Hint

Use `alloc_wait` argument to control the number of ticks after which the allocation should be placed. The default is `1`. Passing `0` will place the allocation at the last tick in the index range, which should be used with caution when optimizing based on the close price.

Let's validate the allocation that was generated based on the first month of data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-55-1)>>> start_idx = pfo.alloc_records.values[0]["start_idx"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-55-2)>>> end_idx = pfo.alloc_records.values[0]["end_idx"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-55-3)>>> close_period = data.get("Close").iloc[start_idx:end_idx]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-55-4)>>> close_period.vbt.rebase(1).vbt.plot().show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/close_period.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/close_period.dark.svg#only-dark)

We see that `ADAUSDT` recorded the highest return and `XRPUSDT` the lowest, which has been correctly translated into the allocation of only 6% to the former and 33% to the latter.

Having index ranges instead of index points stored in a [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) instance also opens new metrics and subplots:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-1)>>> pfo.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-2)Start 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-3)End 2020-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-4)Period 365 days 06:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-5)Total Records 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-6)Coverage 0.915593 << ranges cover 92%
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-7)Overlap Coverage 0.0 << ranges do not overlap
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-8)Mean Allocation: ADAUSDT 0.181818
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-9)Mean Allocation: BNBUSDT 0.212121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-10)Mean Allocation: BTCUSDT 0.218182
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-11)Mean Allocation: ETHUSDT 0.163636
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-12)Mean Allocation: XRPUSDT 0.224242
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-13)Name: group, dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-56-15)>>> pfo.plots().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/plots.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/plots.dark.svg#only-dark)

In the graph above we see not only when each re-allocation takes place, but also which index range that re-allocation is based upon.

All other features such as [support for groups](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#groups) are identical to [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func).


# Waiting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#waiting "Permanent link")

By default, when generating weights over a specific time period, the weights will be allocated at the next possible timestamp. This has some implications. For example, when calling [PortfolioOptimizer.from_optimize_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_optimize_func) without any arguments, it will optimize over the whole time period but return no allocations because there is no next timestamp to allocate the generated weights at:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-1)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-3)... inv_rank_optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-4)... vbt.Takeable(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-6)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-7)Empty DataFrame
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-8)Columns: [BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, ADAUSDT]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-57-9)Index: []
 
[/code]

The solution is to set the waiting time to zero:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-1)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-2)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-3)... inv_rank_optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-4)... vbt.Takeable(data.get("Close")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-5)... alloc_wait=0 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-7)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-8)symbol BTCUSDT ETHUSDT BNBUSDT XRPUSDT ADAUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-9)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-58-10)2020-12-31 23:00:00+00:00 0.2 0.066667 0.266667 0.333333 0.133333
 
[/code]

 1. 


# Numba[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#numba_1 "Permanent link")

Let's perform both the iteration and optimization strictly using Numba. The only difference compared to a Numba-compiled allocation function is that an optimization function takes two arguments instead of one: range start and end index. Under the hood, the iteration and execution is performed by [optimize_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/nb/#vectorbtpro.portfolio.pfopt.nb.optimize_meta_nb).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-2)... def inv_rank_optimize_func_nb(i, start_idx, end_idx, price):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-3)... price_period = price[start_idx:end_idx]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-4)... first_price = price_period[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-5)... last_price = price_period[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-6)... ret = (last_price - first_price) / first_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-7)... ranks = vbt.nb.rank_1d_nb(-ret) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-8)... return ranks / ranks.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-10)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-11)... symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-12)... inv_rank_optimize_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-13)... data.get("Close").values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-14)... every="M",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-15)... jitted_loop=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-18)>>> pfo.allocations
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-19)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-20)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-21)2020-02-01 00:00:00+00:00 0.066667 0.200000 0.266667 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-22)2020-03-01 00:00:00+00:00 0.333333 0.133333 0.266667 0.066667 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-23)2020-04-01 00:00:00+00:00 0.266667 0.200000 0.133333 0.333333 0.066667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-24)2020-05-01 00:00:00+00:00 0.066667 0.200000 0.266667 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-25)2020-06-01 00:00:00+00:00 0.066667 0.266667 0.200000 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-26)2020-07-01 00:00:00+00:00 0.066667 0.266667 0.200000 0.133333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-27)2020-08-01 00:00:00+00:00 0.066667 0.266667 0.333333 0.133333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-28)2020-09-01 00:00:00+00:00 0.333333 0.133333 0.266667 0.066667 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-29)2020-10-01 00:00:00+00:00 0.266667 0.066667 0.133333 0.333333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-30)2020-11-01 00:00:00+00:00 0.333333 0.266667 0.066667 0.133333 0.200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/#__codelineno-59-31)2020-12-01 00:00:00+00:00 0.133333 0.333333 0.266667 0.200000 0.066667
 
[/code]

 1. 2. 

The adaptation to Numba is rather easy, right? ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)

But the speedup from such compilation is immense, especially when tons of re-allocation steps and/or parameter combinations are involved. Try it for yourself!

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/portfolio-optimization/index.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PortfolioOptimization.ipynb)