# MTF analysis[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#mtf-analysis "Permanent link")

By limiting ourselves to only one time frame, we may lose sight of the larger trend, miss clear levels of support and resistance, and overlook high probability entry and stop levels. Monitoring the same pair under different time frames (or time compressions) can help us identify the overall flow of an asset ([the trend is your friend](https://www.investopedia.com/articles/forex/05/050505.asp), after all) and key chart patterns. In fact, all technical indicators will show different results when used in certain times, and all those results combined can make us draw a more complete picture of the market we're participating in.


# Resampling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#resampling "Permanent link")

Since vectorbt is all about time series, the main operation that allows us to switch between different time frames is called _resampling_. There are two types of resampling: upsampling and downsampling.

[Upsampling](https://en.wikipedia.org/wiki/Upsampling) brings a time series to a shorter time frame (i.e., a higher frequency), such as by converting a daily price to an hourly price. The prefix "up" here means an increase in the number of data points. This operation isn't associated with any information loss since none of the data is removed, just re-indexed: the value at each day appears at the very first hour in the upsampled array, while all other hours contain NaN. By forward-filling those NaN values, we would be able to compare any daily time series with an hourly time series!

(Reload the page if the diagram doesn't show up)

[Downsampling](https://en.wikipedia.org/wiki/Downsampling_\(signal_processing\)), on the other hand, brings a time series to a longer time frame (i.e., a lower frequency), such as by converting an hourly price to a daily price. The prefix "down" here means a decrease in the number of data points. In contrast to upsampling, downsampling **results in information loss** since multiple pieces of information are aggregated into a single one. That's why time frames are also referred to as time compressions. But even though we lose some information, we can now observe a bigger trend!

Hint

Downsampling is a similar concept to a moving average, which aggregates information at each time step to reveal a bigger trend.


# Data[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#data "Permanent link")

Before pulling any data, we need to ask ourselves: _"What is the shortest time frame we want to analyze?"_ Once this question is answered, we need to pull the data of this exact granularity. For example, to be able to work with the time frames `H1` (1 hour), `H4` (4 hours), and `D1` (1 day), we need data with at least the time frame `H1`, which can be later downsampled to derive the `H4` and `D1` time frames.

Note

This wouldn't work the other way around: we cannot upsample `H4` or `D1` to derive `H1` since most data points would just become NaN.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-3)>>> h1_data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-4)... "BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-5)... start="2020-01-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-6)... end="2021-01-01 UTC",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-7)... timeframe="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-0-8)... )
 
[/code]

Period 18/18

Let's persist the data locally to avoid re-fetching it every time we start a new runtime:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-1-1)>>> h1_data.to_hdf()
 
[/code]

We can then access the saved data easily using [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-2-1)>>> h1_data = vbt.HDFData.pull("BinanceData.h5")
 
[/code]

Let's take a look at the index of the data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-1)>>> h1_data.wrapper.index 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-2)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-01 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-3) '2020-01-01 02:00:00+00:00', '2020-01-01 03:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-4) '2020-01-01 04:00:00+00:00', '2020-01-01 05:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-6) '2020-12-31 18:00:00+00:00', '2020-12-31 19:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-7) '2020-12-31 20:00:00+00:00', '2020-12-31 21:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-8) '2020-12-31 22:00:00+00:00', '2020-12-31 23:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-3-9) dtype='datetime64[ns, UTC]', name='Open time', length=8767, freq=None)
 
[/code]

 1. 

As expected, the index starts at midnight of 1st January and ends at 11 PM on December 31. But what about `freq=None`? Pandas wasn't able to derive the frequency of data because some data points seem to be missing. This happens relatively often and indicates that the exchange was down. To get all the missing indices, we need to create a resampler of type [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) and then use [Resampler.index_difference](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.index_difference) with `reverse=True`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-1)>>> h1_resampler = h1_data.wrapper.get_resampler("1h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-2)>>> h1_resampler.index_difference(reverse=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-3)DatetimeIndex(['2020-02-09 02:00:00+00:00', '2020-02-19 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-4) '2020-02-19 13:00:00+00:00', '2020-02-19 14:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-5) '2020-02-19 15:00:00+00:00', '2020-02-19 16:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-6) '2020-03-04 10:00:00+00:00', '2020-04-25 02:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-7) '2020-04-25 03:00:00+00:00', '2020-06-28 02:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-8) '2020-06-28 03:00:00+00:00', '2020-06-28 04:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-9) '2020-11-30 06:00:00+00:00', '2020-12-21 15:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-10) '2020-12-21 16:00:00+00:00', '2020-12-21 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-11) '2020-12-25 02:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-4-12) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 

Those are the time periods when Binance was supposedly down. The good news is: we don't need to set those data points to NaN since vectorbt accepts missing indices just fine. In fact, marking those points as missing would only inflate the data and make working with indicators that don't like missing data much, such as TA-Lib, prone to errors.

Now, how do we downsample that data to `H4` and `D1`? If we look at the columns stored in the data instance, we'd see very familiar column names `Open`, `High`, `Low`, `Close`, and `Volume`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-5-1)>>> h1_data.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-5-2)Index(['Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote volume',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-5-3) 'Number of trades', 'Taker base volume', 'Taker quote volume'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-5-4) dtype='object')
 
[/code]

First, let's remove columns that aren't much interesting to us right now:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-6-1)>>> h1_ohlcv_data = h1_data[["Open", "High", "Low", "Close", "Volume"]]
 
[/code]

The most conventional way to resample any OHLCV data is by using Pandas:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-1)>>> h4_ohlcv = h1_ohlcv_data.get().resample("4h").agg({ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-2)... "Open": "first",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-3)... "High": "max",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-4)... "Low": "min",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-5)... "Close": "last",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-6)... "Volume": "sum"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-7)... })
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-8)>>> h4_ohlcv
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-9) Open High Low Close \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-11)2020-01-01 00:00:00+00:00 7195.24 7245.00 7175.46 7225.01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-12)2020-01-01 04:00:00+00:00 7225.00 7236.27 7199.11 7209.83 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-13)2020-01-01 08:00:00+00:00 7209.83 7237.73 7180.00 7197.20 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-14)... ... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-15)2020-12-31 12:00:00+00:00 28910.29 28989.03 27850.00 28770.00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-16)2020-12-31 16:00:00+00:00 28782.01 29000.00 28311.00 28897.83 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-17)2020-12-31 20:00:00+00:00 28897.84 29169.55 28780.00 28923.63 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-19) Volume 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-20)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-21)2020-01-01 00:00:00+00:00 2833.749180 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-22)2020-01-01 04:00:00+00:00 2061.295051 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-23)2020-01-01 08:00:00+00:00 3166.654361 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-24)... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-25)2020-12-31 12:00:00+00:00 19597.147389 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-26)2020-12-31 16:00:00+00:00 10279.179141 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-27)2020-12-31 20:00:00+00:00 7875.879035 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-7-29)[2196 rows x 5 columns]
 
[/code]

 1. 

We see that the time interval has increased from 1 hour to 4 hours; in fact, we just built 1 bigger bar out of 4 smaller ones:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-1)>>> h1_ohlcv_data.get().iloc[:4]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-2) Open High Low Close Volume
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-3)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-4)2020-01-01 00:00:00+00:00 7195.24 7196.25 7175.46 7177.02 511.814901
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-5)2020-01-01 01:00:00+00:00 7176.47 7230.00 7175.71 7216.27 883.052603
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-6)2020-01-01 02:00:00+00:00 7215.52 7244.87 7211.41 7242.85 655.156809
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-7)2020-01-01 03:00:00+00:00 7242.66 7245.00 7220.00 7225.01 783.724867
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-9)>>> h4_ohlcv.iloc[[0]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-10) Open High Low Close Volume
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-11)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-8-12)2020-01-01 00:00:00+00:00 7195.24 7245.0 7175.46 7225.01 2833.74918
 
[/code]

Great! But as with everything, vectorbt deploys special methods that either do such things more efficiently or more flexibly (mostly both). 

Remember how most classes in vectorbt subclass [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable)? In turn, this class subclasses [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping), which is designed for managing all the Pandas objects stored in a class instance. Since it also contains the Pandas metadata such as index and columns, we can use that index for resampling. Particularly, any subclass of [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping) has an abstract method [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample), which can be overridden to resample complex vectorbt objects, such as instances of [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) and [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio).

Luckily for us, vectorbt has implemented this method in most classes that can actually be resampled. In most cases, it forwards most arguments and keyword arguments to [Wrapping.get_resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.get_resampler) to build a resampler, and then applies this resampler on all Pandas objects stored in a vectorbt object. Continuing with data, [Data.resample](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.resample) looks for any OHLCV columns in a data instance and resamples them automatically. But what happens with other columns, such as `Number of trades`? Their resampling function can be defined in the feature config [Data.feature_config](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.feature_config). Even better: vectorbt has defined resampling functions for all columns of all remote data classes!

Let's take a look at the feature config of [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-1)>>> print(vbt.prettify(vbt.BinanceData.feature_config))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-2)Config({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-3) 'Close time': {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-4) 'resample_func': <function BinanceData.<lambda> at 0x7fd2d60c4378>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-5) },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-6) 'Quote volume': {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-7) 'resample_func': <function BinanceData.<lambda> at 0x7fd2d60c4400>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-8) },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-9) 'Number of trades': {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-10) 'resample_func': <function BinanceData.<lambda> at 0x7fd2d60c4488>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-11) },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-12) 'Taker base volume': {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-13) 'resample_func': <function BinanceData.<lambda> at 0x7fd2d60c4510>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-14) },
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-15) 'Taker quote volume': {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-16) 'resample_func': <function BinanceData.<lambda> at 0x7fd2d60c4598>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-17) }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-9-18)})
 
[/code]

Each of those lambda functions takes the Pandas object and the resampler, and performs the operation using [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply).

Hint

There is no need to define resampling functions for OHLCV columns as vectorbt already knows what to do.

Let's downsample `H1` to `H4` and `D1` with a single line of code:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-10-1)>>> h1_data.use_feature_config_of(vbt.BinanceData) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-10-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-10-3)>>> h4_data = h1_data.resample("4h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-10-4)>>> d1_data = h1_data.resample("1d")
 
[/code]

 1. 

That's it!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-1)>>> d1_data.get().iloc[[0, -1]] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-2) Open High Low Close \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-3)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-4)2020-01-01 00:00:00+00:00 7195.24 7255.0 7175.15 7200.85 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-5)2020-12-31 00:00:00+00:00 28875.55 29300.0 27850.00 28923.63 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-7) Volume Quote volume Trade count \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-8)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-9)2020-01-01 00:00:00+00:00 16792.388165 1.212145e+08 194010 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-10)2020-12-31 00:00:00+00:00 75508.505152 2.173600e+09 1552793 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-12) Taker base volume Taker quote volume 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-14)2020-01-01 00:00:00+00:00 8946.955535 6.459779e+07 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-11-15)2020-12-31 00:00:00+00:00 36431.622080 1.049389e+09 
 
[/code]

 1. 

We can validate the results from resampling by comparing them against the same time frame fetched directly from Binance:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-1)>>> vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-2)... "BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-3)... start="2020-01-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-4)... end="2021-01-01 UTC",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-5)... timeframe="1d"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-12-6)... ).get().iloc[[0, -1]]
 
[/code]

100%
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-1) Open High Low Close \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-2)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-3)2020-01-01 00:00:00+00:00 7195.24 7255.0 7175.15 7200.85 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-4)2020-12-31 00:00:00+00:00 28875.55 29300.0 27850.00 28923.63 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-6) Volume Quote volume Trade count \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-7)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-8)2020-01-01 00:00:00+00:00 16792.388165 1.212145e+08 194010 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-9)2020-12-31 00:00:00+00:00 75508.505152 2.173600e+09 1552793 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-11) Taker base volume Taker quote volume 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-12)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-13)2020-01-01 00:00:00+00:00 8946.955535 6.459779e+07 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/#__codelineno-13-14)2020-12-31 00:00:00+00:00 36431.622080 1.049389e+09
 
[/code]

Our data instance just resampled itself the same way as done by Binance ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/mtf-analysis/index.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/MTFAnalysis.ipynb)