# SuperFast SuperTrend[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#superfast-supertrend "Permanent link")

While Python is slower than many compiled languages, it's easy to use and extremely diverse. For many, especially in the data science domain, the practicality of the language beats the speed considerations - it's like a Swiss army knife for programmers and researchers alike.

Unfortunately for quants, Python becomes a real bottleneck when iterating over (a large amount of) data. For this reason, there is an entire ecosystem of scientific packages such as NumPy and Pandas, which are highly optimized for performance, with critical code paths often written in Cython or C. Those packages mostly work on arrays, giving us a common interface for processing data in an efficient manner. 

This ability is highly appreciated when constructing indicators that can be translated into a set of vectorized operations, such as [OBV](https://www.investopedia.com/terms/o/onbalancevolume.asp). But even non-vectorized operations, such as the exponential weighted moving average (EMA) powering numerous indicators such as [MACD](https://www.investopedia.com/terms/m/macd.asp), were implemented in a compiled language and are offered as a ready-to-use Python function. But sometimes, an indicator is difficult or even impossible to develop solely using standard array operations because the indicator introduces a path dependency, where a decision today depends upon a decision made yesterday. One member of such a family of indicators is SuperTrend.

In this example, you will learn how to design and implement a SuperTrend indicator, and gradually optimize it towards a never-seen performance using [TA-Lib](https://github.com/mrjbq7/ta-lib) and [Numba](http://numba.pydata.org/). We will also backtest the newly created indicator on a range of parameters using vectorbt (PRO).


# Data[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#data "Permanent link")

The first step is always getting the (right) data. In particular, we need a sufficient amount of data to benchmark different SuperTrend implementations. Let's pull 2 years of hourly Bitcoin and Ethereum data from Binance using the vectorbt's [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData) class:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-3)>>> data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-4)... ['BTCUSDT', 'ETHUSDT'], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-5)... start='2020-01-01 UTC',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-6)... end='2022-01-01 UTC',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-7)... timeframe='1h'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-0-8)... )
 
[/code]

Symbol 2/2

Period 36/36

The fetching operation for both symbols took us around 80 seconds to complete. Since Binance, as any other exchange, will never return the whole data at once, vectorbt first requested the maximum amount of data starting on January 1st, 2020 and then gradually collected the remaining data by also respecting the Binance's API rate limits. In total, this resulted in 36 requests per symbol. Finally, vectorbt aligned both symbols in case their indexes or columns were different and made the final index timezone-aware (in UTC).

To avoid repeatedly hitting the Binance servers each time we start a new Python session, we should save the downloaded data locally using either the vectorbt's [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv) or [Data.to_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_hdf):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-1-1)>>> data.to_hdf('my_data.h5')
 
[/code]

We can then access the saved data easily using [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-2-1)>>> data = vbt.HDFData.pull('my_data.h5')
 
[/code]

Symbol 2/2

Hint

We can access any of the symbols in an HDF file using regular path expressions. For example, the same as above: `vbt.HDFData.pull(['my_data.h5/BTCUSDT', 'my_data.h5/ETHUSDT'])`.

Once we have the data, let's take a quick look at what's inside. To get any of the stored DataFrames, use the [Data.data](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/#vectorbtpro.data.base.Data.data) dictionary with each DataFrame keyed by symbol:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-1)>>> data.data['BTCUSDT'].info()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-2)<class 'pandas.core.frame.DataFrame'>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-3)DatetimeIndex: 17514 entries, 2019-12-31 23:00:00+00:00 to 2021-12-31 22:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-4)Data columns (total 10 columns):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-5) # Column Non-Null Count Dtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-6)--- ------ -------------- ----- 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-7) 0 Open 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-8) 1 High 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-9) 2 Low 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-10) 3 Close 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-11) 4 Volume 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-12) 5 Close time 17514 non-null datetime64[ns, UTC]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-13) 6 Quote volume 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-14) 7 Number of trades 17514 non-null int64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-15) 8 Taker base volume 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-16) 9 Taker quote volume 17514 non-null float64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-17)dtypes: datetime64[ns, UTC](1), float64(8), int64(1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-3-18)memory usage: 2.0 MB
 
[/code]

We can also get an overview of all the symbols captured:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-1)>>> data.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-2)Start 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-3)End 2021-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-4)Period 17513
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-5)Total Symbols 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-6)Last Index: BTCUSDT 2021-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-7)Last Index: ETHUSDT 2021-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-8)Null Counts: BTCUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-9)Null Counts: ETHUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-4-10)Name: agg_stats, dtype: object
 
[/code]

Each symbol has 17513 data points with no NaNs - good!

If you ever worked with vectorbt, you would know that vectorbt loves the data to be supplied with symbols as columns - one per backtest - rather than features as columns. Since SuperTrend depends upon the high, low, and close price, let's get those three features as separate DataFrames using [Data.get](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/#vectorbtpro.data.base.Data.get):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-1)>>> high = data.get('High')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-2)>>> low = data.get('Low')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-3)>>> close = data.get('Close')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-5)>>> close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-6)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-7)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-8)2020-01-01 00:00:00+00:00 7177.02 128.87
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-9)2020-01-01 01:00:00+00:00 7216.27 130.64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-10)2020-01-01 02:00:00+00:00 7242.85 130.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-11)2020-01-01 03:00:00+00:00 7225.01 130.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-12)2020-01-01 04:00:00+00:00 7217.27 130.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-13)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-14)2021-12-31 19:00:00+00:00 45728.28 3626.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-15)2021-12-31 20:00:00+00:00 45879.24 3645.04
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-16)2021-12-31 21:00:00+00:00 46333.86 3688.41
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-17)2021-12-31 22:00:00+00:00 46303.99 3681.80
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-18)2021-12-31 23:00:00+00:00 46216.93 3676.23
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-5-20)[17513 rows x 2 columns]
 
[/code]

Hint

To get a column of a particular symbol as a Series, use `data.get('Close', 'BTCUSDT')`.

We're all set to design our first SuperTrend indicator!


# Design[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#design "Permanent link")

SuperTrend is a trend-following indicator that uses Average True Range ([ATR](https://en.wikipedia.org/wiki/Average_true_range)) and [median price](https://www.incrediblecharts.com/indicators/median_price.php) to define a set of upper and lower bands. The idea is rather simple: when the close price crosses above the upper band, the asset is considered to be entering an uptrend, hence a buy signal. When the close price crosses below the lower band, the asset is considered to have exited the uptrend, hence a sell signal. 

Unlike the idea, the calculation procedure is anything but simple:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-1)BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-2)BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-4)FINAL UPPERBAND = IF (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-5) THEN Current BASIC UPPERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-6) ELSE Previous FINAL UPPERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-7)FINAL LOWERBAND = IF (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-8) THEN Current BASIC LOWERBAND 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-9) ELSE Previous FINAL LOWERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-11)SUPERTREND = IF (Previous SUPERTREND == Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-12) THEN Current FINAL UPPERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-13) ELIF (Previous SUPERTREND == Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-14) THEN Current FINAL LOWERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-15) ELIF (Previous SUPERTREND == Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-16) THEN Current FINAL LOWERBAND
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-17) ELIF (Previous SUPERTREND == Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-6-18) THEN Current FINAL UPPERBAND
 
[/code]

Even though the basic bands can be well computed using the standard tools, you'll certainly get a headache when attempting to do this for the final bands. The consensus among most open-source solutions is to use a basic Python for-loop and write the array elements one at a time. But is this scalable? We're here to find out!


# Pandas[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#pandas "Permanent link")

[Pandas](https://github.com/pandas-dev/pandas) is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool. Since it's a go-to library for processing data in Python, let's write our first implementation using Pandas alone. It will take one column and one combination of parameters, and return four arrays: one for the SuperTrend (`trend`), one for the direction (`dir_`), one for the uptrend (`long`), and one for the downtrend (`short`). We'll also split the implementation into 5 parts for readability and to be able to optimize any component at any time:

 1. Calculation of the median price - `get_med_price`
 2. Calculation of the ATR - `get_atr`
 3. Calculation of the basic bands - `get_basic_bands`
 4. Calculation of the final bands - `get_final_bands`
 5. Putting all puzzles together - `supertrend`

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-1)>>> def get_med_price(high, low):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-2)... return (high + low) / 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-4)>>> def get_atr(high, low, close, period):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-5)... tr0 = abs(high - low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-6)... tr1 = abs(high - close.shift())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-7)... tr2 = abs(low - close.shift())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-8)... tr = pd.concat((tr0, tr1, tr2), axis=1).max(axis=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-9)... atr = tr.ewm(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-10)... alpha=1 / period, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-11)... adjust=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-12)... min_periods=period).mean() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-13)... return atr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-15)>>> def get_basic_bands(med_price, atr, multiplier):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-16)... matr = multiplier * atr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-17)... upper = med_price + matr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-18)... lower = med_price - matr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-19)... return upper, lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-21)>>> def get_final_bands(close, upper, lower): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-22)... trend = pd.Series(np.full(close.shape, np.nan), index=close.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-23)... dir_ = pd.Series(np.full(close.shape, 1), index=close.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-24)... long = pd.Series(np.full(close.shape, np.nan), index=close.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-25)... short = pd.Series(np.full(close.shape, np.nan), index=close.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-26)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-27)... for i in range(1, close.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-28)... if close.iloc[i] > upper.iloc[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-29)... dir_.iloc[i] = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-30)... elif close.iloc[i] < lower.iloc[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-31)... dir_.iloc[i] = -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-32)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-33)... dir_.iloc[i] = dir_.iloc[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-34)... if dir_.iloc[i] > 0 and lower.iloc[i] < lower.iloc[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-35)... lower.iloc[i] = lower.iloc[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-36)... if dir_.iloc[i] < 0 and upper.iloc[i] > upper.iloc[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-37)... upper.iloc[i] = upper.iloc[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-38)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-39)... if dir_.iloc[i] > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-40)... trend.iloc[i] = long.iloc[i] = lower.iloc[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-41)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-42)... trend.iloc[i] = short.iloc[i] = upper.iloc[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-43)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-44)... return trend, dir_, long, short
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-45)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-46)>>> def supertrend(high, low, close, period=7, multiplier=3):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-47)... med_price = get_med_price(high, low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-48)... atr = get_atr(high, low, close, period)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-49)... upper, lower = get_basic_bands(med_price, atr, multiplier)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-7-50)... return get_final_bands(close, upper, lower)
 
[/code]

 1. 2. 3. 4. 

Let's run the `supertrend` function on the `BTCUSDT` symbol:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-1)>>> supert, superd, superl, supers = supertrend(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-2)... high['BTCUSDT'], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-3)... low['BTCUSDT'], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-4)... close['BTCUSDT']
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-7)>>> supert
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-8)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-9)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-10)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-11)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-12) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-13)2021-12-31 21:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-14)2021-12-31 22:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-15)2021-12-31 23:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-16)Length: 17513, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-18)>>> superd 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-19)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-20)2020-01-01 00:00:00+00:00 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-21)2020-01-01 01:00:00+00:00 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-22)2020-01-01 02:00:00+00:00 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-23) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-24)2021-12-31 21:00:00+00:00 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-25)2021-12-31 22:00:00+00:00 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-26)2021-12-31 23:00:00+00:00 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-27)Length: 17513, dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-29)>>> superl 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-30)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-31)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-32)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-33)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-34) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-35)2021-12-31 21:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-36)2021-12-31 22:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-37)2021-12-31 23:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-38)Length: 17513, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-39)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-40)>>> supers 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-41)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-42)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-43)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-44)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-45) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-46)2021-12-31 21:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-47)2021-12-31 22:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-48)2021-12-31 23:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-8-49)Length: 17513, dtype: float64
 
[/code]

 1. 2. 3. 

If you print out the head of the `supert` Series using `supert.head(10)`, you'll notice that the first 6 data points are all NaN. This is because the ATR's rolling period is 7, so the first 6 computed windows contained incomplete data.

A graph is worth 1,000 words. Let's plot the first month of data (January 2020):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-9-1)>>> date_range = slice('2020-01-01', '2020-02-01')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-9-2)>>> fig = close.loc[date_range, 'BTCUSDT'].rename('Close').vbt.plot() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-9-3)>>> supers.loc[date_range].rename('Short').vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-9-4)>>> superl.loc[date_range].rename('Long').vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-9-5)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/pandas.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/pandas.dark.svg#only-dark)

We've generated and visualized the SuperTrend values, but what about performance? Can we already make our overfitting machine with thousands of parameter combinations rolling? Not so fast. As you might have guessed, the `supertrend` function takes some time to compute:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-10-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-10-2)>>> supertrend(high['BTCUSDT'], low['BTCUSDT'], close['BTCUSDT'])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-10-3)2.15 s ± 19.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

Ouch! Doing 1000 backtests would take us roughly 33 minutes. 

Let's hear what Pandas TA has to say about this:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-11-1)>>> SUPERTREND = vbt.pandas_ta('SUPERTREND') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-11-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-11-3)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-11-4)>>> SUPERTREND.run(high['BTCUSDT'], low['BTCUSDT'], close['BTCUSDT'])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-11-5)784 ms ± 14.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 

That's a 3x speedup, mostly due to the fact that Pandas TA uses ATR from TA-Lib. 

Is it now acceptable? Of course not ![💢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a2.svg) Can we get better than this? Hell yeah!


# NumPy + Numba = ![❤](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2764.svg)[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#numpy-numba "Permanent link")

Pandas shines whenever it comes to manipulating heterogeneous tabular data, but is this really applicable to indicators? You might have noticed that even though we used Pandas, none of the operations in any of our newly defined functions makes use of index or column labels. Moreover, most indicators take, manipulate, and return arrays of the same dimensions and shape, which makes indicator development a purely algebraic challenge that can be well decomposed into multiple vectorized steps or solved on the per-element basis (or both!). Given that Pandas just extends NumPy and the latter is considered as a faster (although lower level) package, let's adapt our logic to NumPy arrays instead.

Both functions `get_med_price` and `get_basic_bands` are based on basic arithmetic computations such as addition and multiplication, which are applicable to both Pandas and NumPy arrays and require no further changes. But what about `get_atr` and `get_final_bands`? The former can be re-implemented using NumPy and vectorbt's own arsenal of Numba-compiled functions:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-1)>>> def get_atr_np(high, low, close, period):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-2)... shifted_close = vbt.nb.fshift_1d_nb(close) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-3)... tr0 = np.abs(high - low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-4)... tr1 = np.abs(high - shifted_close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-5)... tr2 = np.abs(low - shifted_close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-6)... tr = np.column_stack((tr0, tr1, tr2)).max(axis=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-7)... atr = vbt.nb.wwm_mean_1d_nb(tr, period) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-12-8)... return atr
 
[/code]

 1. 2. 3. 

The latter, on the other hand, is an iterative algorithm - it's rather a poor fit for NumPy and an ideal fit for Numba, which can easily run for-loops at a machine code speed:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-2)... def get_final_bands_nb(close, upper, lower): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-3)... trend = np.full(close.shape, np.nan) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-4)... dir_ = np.full(close.shape, 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-5)... long = np.full(close.shape, np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-6)... short = np.full(close.shape, np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-7)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-8)... for i in range(1, close.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-9)... if close[i] > upper[i - 1]: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-10)... dir_[i] = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-11)... elif close[i] < lower[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-12)... dir_[i] = -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-13)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-14)... dir_[i] = dir_[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-15)... if dir_[i] > 0 and lower[i] < lower[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-16)... lower[i] = lower[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-17)... if dir_[i] < 0 and upper[i] > upper[i - 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-18)... upper[i] = upper[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-19)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-20)... if dir_[i] > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-21)... trend[i] = long[i] = lower[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-22)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-23)... trend[i] = short[i] = upper[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-24)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-13-25)... return trend, dir_, long, short
 
[/code]

 1. 2. 3. 

If you look at the function above, you'll notice that 1) it's a regular Python code that can run even without being decorated with `@njit`, and 2) it's almost identical to the implementation with Pandas - the main difference is in each `iloc[...]` being replaced by `[...]`. We can write a simple Python function that operates on constants and NumPy arrays, and Numba will try to make it **much** faster, fully automatically. Isn't that impressive? 

Let's look at the result of this refactoring:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-1)>>> def faster_supertrend(high, low, close, period=7, multiplier=3):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-2)... med_price = get_med_price(high, low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-3)... atr = get_atr_np(high, low, close, period)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-4)... upper, lower = get_basic_bands(med_price, atr, multiplier)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-5)... return get_final_bands_nb(close, upper, lower)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-7)>>> supert, superd, superl, supers = faster_supertrend(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-8)... high['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-9)... low['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-10)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-13)>>> supert
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-14)array([ nan, nan, nan, ..., 47608.3465635,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-15) 47608.3465635, 47608.3465635])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-16)>>> superd
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-17)array([ 1, 1, 1, ..., -1, -1, -1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-19)>>> superl
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-20)array([nan, nan, nan, ..., nan, nan, nan])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-22)>>> supers
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-23)array([ nan, nan, nan, ..., 47608.3465635,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-14-24) 47608.3465635, 47608.3465635])
 
[/code]

 1. 

Info

When executing a Numba-decorated function for the first time, it may take longer due to compilation.

As expected, those are arrays similar to the ones returned by the `supertrend` function, just without any labels. To attach labels, we can simply do:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-1)>>> pd.Series(supert, index=close.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-3)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-4)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-5)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-6) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-7)2021-12-31 21:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-8)2021-12-31 22:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-9)2021-12-31 23:00:00+00:00 47608.346563
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-15-10)Length: 17513, dtype: float64
 
[/code]

Wondering how much our code has gained in performance? Wonder no more:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-1)%%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-2)>>> faster_supertrend(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-3)... high['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-4)... low['BTCUSDT'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-5)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-16-7)1.11 ms ± 7.05 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
[/code]

That's a 780x speedup over an average Pandas TA run ![😈](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f608.svg)


# NumPy + Numba + TA-Lib = ![⚡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/26a1.svg)[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#numpy-numba-talib "Permanent link")

If you think that this result cannot be topped, then apparently you haven't worked with TA-Lib. Even though there is no SuperTrend indicator available in TA-Lib, we can still use its highly-optimized indicator functions for intermediate calculations. In particular, instead of reinventing the wheel and implementing the median price and ATR functionality from scratch, we can use the `MEDPRICE` and `ATR` TA-Lib functions respectively. They have two major advantages over our custom implementation:

 1. Single pass through data
 2. No compilation overhead from Numba

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-1)>>> import talib
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-3)>>> def faster_supertrend_talib(high, low, close, period=7, multiplier=3):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-4)... avg_price = talib.MEDPRICE(high, low) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-5)... atr = talib.ATR(high, low, close, period)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-6)... upper, lower = get_basic_bands(avg_price, atr, multiplier)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-7)... return get_final_bands_nb(close, upper, lower)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-9)>>> faster_supertrend_talib(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-10)... high['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-11)... low['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-12)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-14)(array([ nan, nan, nan, ..., 47608.3465635,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-15) 47608.3465635, 47608.3465635]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-16) array([ 1, 1, 1, ..., -1, -1, -1]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-17) array([nan, nan, nan, ..., nan, nan, nan]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-18) array([ nan, nan, nan, ..., 47608.3465635,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-19) 47608.3465635, 47608.3465635]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-21)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-22)>>> faster_supertrend_talib(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-23)... high['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-24)... low['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-25)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-17-27)253 µs ± 815 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
[/code]

 1. 

Another 4x improvement - by the time another trader processed a single column of data, we would have processed around 3 thousand columns. Agreed, the speed of our indicator is slowly getting ridiculously high ![😄](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f604.svg)


# Indicator factory[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#indicator-factory "Permanent link")

Let's stop here and ask ourselves: why do we even need such a crazy performance? 

That's when parameter optimization comes into play. The two parameters that we have - `period` and `multiplier` \- are the default values commonly used in technical analysis. But what makes those values universal and how do we know whether there aren't any better values for the markets we're participating in? Imagine having a pipeline that can backtest hundreds or even thousands of parameters and reveal configurations and market regimes that correlate better on average?

[IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory) is a vectorbt's own powerhouse that can make any indicator function parametrizable. To get a better idea of what this means, let's supercharge the `faster_supertrend_talib` function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-1)>>> SuperTrend = vbt.IF(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-2)... class_name='SuperTrend',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-3)... short_name='st',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-4)... input_names=['high', 'low', 'close'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-5)... param_names=['period', 'multiplier'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-6)... output_names=['supert', 'superd', 'superl', 'supers']
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-7)... ).with_apply_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-8)... faster_supertrend_talib, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-9)... takes_1d=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-10)... period=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-11)... multiplier=3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-18-12)... )
 
[/code]

 1. 2. 

The indicator factory is a class that can generate so-called indicator classes. You can imagine it being a conveyor belt that can take a specification of your indicator function and produce a stand-alone Python class for running that function in a very flexible way. In our example, when we called `vbt.IF(...)`, it has internally created an indicator class `SuperTrend`, and once we supplied `faster_supertrend_talib` to [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.with_apply_func), it attached a method `SuperTrend.run` for running the indicator. Let's try it out!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-1)>>> vbt.phelp(SuperTrend.run) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-2)SuperTrend.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-3) high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-4) low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-5) close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-6) period=Default(value=7),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-7) multiplier=Default(value=3),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-8) short_name='st',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-9) hide_params=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-10) hide_default=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-11) **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-12)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-13) Run `SuperTrend` indicator.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-15) * Inputs: `high`, `low`, `close`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-16) * Parameters: `period`, `multiplier`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-17) * Outputs: `supert`, `superd`, `superl`, `supers`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-19) Pass a list of parameter names as `hide_params` to hide their column levels.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-20) Set `hide_default` to False to show the column levels of the parameters with a default value.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-22) Other keyword arguments are passed to `SuperTrend.run_pipeline`.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-24)>>> st = SuperTrend.run(high, low, close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-25)>>> st.supert
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-26)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-27)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-28)2020-01-01 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-29)2020-01-01 01:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-30)2020-01-01 02:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-31)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-32)2021-12-31 21:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-33)2021-12-31 22:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-34)2021-12-31 23:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-35)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-19-36)[17513 rows x 2 columns]
 
[/code]

 1. 

Notice how our SuperTrend indicator magically accepted two-dimensional Pandas arrays, even though the function itself can only work on one-dimensional NumPy arrays. Not only it computed the SuperTrend on each column, but it also converted the resulting arrays back into the Pandas format for pure convenience. So, how does all of this impact the performance?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-20-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-20-2)>>> SuperTrend.run(high, low, close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-20-3)2 ms ± 130 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]

Not that much! With all the pre- and postprocessing taking place, the indicator needs roughly one millisecond to process one column (that is, 17k data points).


# Expressions[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#expressions "Permanent link")

If you think that calling `vbt.IF(...)` and providing `input_names`, `param_names`, and other information manually is too much work, well, vectorbt has something for you. Our `faster_supertrend_talib` is effectively a black box to the indicator factory - that's why the factory cannot introspect it and derive the required information programmatically. But it easily could if we converted `faster_supertrend_talib` into an [expression](https://realpython.com/python-eval-function/)! 

Expressions are regular strings that can be evaluated into Python code. By giving such a string to [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr), the factory will be able to see what's inside, parse the specification, and generate a full-blown indicator class.

Hint

Instance methods with the prefix `with` (such as `with_apply_func`) require the specification to be provided manually, while class methods with the prefix `from` (such as `from_expr`) can parse this information automatically.

Here's an expression for `faster_supertrend_talib`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-1)>>> expr = """
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-2)... SuperTrend[st]:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-3)... medprice = @talib_medprice(high, low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-4)... atr = @talib_atr(high, low, close, @p_period)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-5)... upper, lower = get_basic_bands(medprice, atr, @p_multiplier)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-6)... supert, superd, superl, supers = get_final_bands(close, upper, lower)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-7)... supert, superd, superl, supers
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-21-8)... """
 
[/code]

Using annotations with `@` we tell the factory how to treat specific variables. For instance, any variable with the prefix `@talib` gets replaced by the respective TA-Lib function that has been upgraded with broadcasting and multidimensionality. You can also see that parameters were annotated with `@p`, while inputs and outputs weren't annotated at all - the factory knows exactly that `high` is the high price, while the latest line apparently returns 4 output objects.

For more examples, see the documentation on expression parsing.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-1)>>> SuperTrend = vbt.IF.from_expr(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-2)... expr, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-3)... takes_1d=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-4)... get_basic_bands=get_basic_bands, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-5)... get_final_bands=get_final_bands_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-6)... period=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-7)... multiplier=3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-10)>>> st = SuperTrend.run(high, low, close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-11)>>> st.supert
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-12)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-14)2020-01-01 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-15)2020-01-01 01:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-16)2020-01-01 02:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-17)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-18)2021-12-31 21:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-19)2021-12-31 22:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-20)2021-12-31 23:00:00+00:00 47608.346563 3770.258246
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-22)[17513 rows x 2 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-24)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-25)>>> SuperTrend.run(high, low, close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-22-26)2.35 ms ± 81.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]

 1. 

By the way, this is exactly how WorldQuant's Alphas are implemented in vectorbt. Never stop loving Python for the magic it enables ![✨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2728.svg)


# Plotting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#plotting "Permanent link")

Remember how we previously plotted SuperTrend? We had to manually select the date range from each output array and add it to the plot by passing the figure around. Let's subclass `SuperTrend` and define a method `plot` that does all of this for us:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-1)>>> class SuperTrend(SuperTrend):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-2)... def plot(self, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-3)... column=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-4)... close_kwargs=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-5)... superl_kwargs=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-6)... supers_kwargs=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-7)... fig=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-8)... **layout_kwargs): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-9)... close_kwargs = close_kwargs if close_kwargs else {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-10)... superl_kwargs = superl_kwargs if superl_kwargs else {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-11)... supers_kwargs = supers_kwargs if supers_kwargs else {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-12)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-13)... close = self.select_col_from_obj(self.close, column).rename('Close')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-14)... supers = self.select_col_from_obj(self.supers, column).rename('Short')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-15)... superl = self.select_col_from_obj(self.superl, column).rename('Long')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-16)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-17)... fig = close.vbt.plot(fig=fig, **close_kwargs, **layout_kwargs) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-18)... supers.vbt.plot(fig=fig, **supers_kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-19)... superl.vbt.plot(fig=fig, **superl_kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-20)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-23-21)... return fig
 
[/code]

 1. 2. 3. 4. 5. 

But how are we supposed to select the date range to plot? Pretty easy: the indicator factory made `SuperTrend` indexable just like any regular Pandas object! Let's plot the same date range and symbol but slightly change the color palette:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-24-1)>>> st = SuperTrend.run(high, low, close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-24-2)>>> st.loc[date_range, 'BTCUSDT'].plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-24-3)... superl_kwargs=dict(trace_kwargs=dict(line_color='limegreen')),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-24-4)... supers_kwargs=dict(trace_kwargs=dict(line_color='red'))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-24-5)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/indicator.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/indicator.dark.svg#only-dark)

Beautiful!


# Backtesting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#backtesting "Permanent link")

Backtesting is usually the simplest step in vectorbt: convert the indicator values into two signal arrays - `entries` and `exits` \- and supply them to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). To make the test better reflect the reality, let's do several adjustments. Since we're calculating the SuperTrend values based on the current close price and vectorbt executes orders right away, we'll shift the execution of the signals by one tick forward:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-25-1)>>> entries = (~st.superl.isnull()).vbt.signals.fshift() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-25-2)>>> exits = (~st.supers.isnull()).vbt.signals.fshift()
 
[/code]

 1. 

We'll also apply the commission of 0.1%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-2)... close=close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-3)... entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-4)... exits=exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-5)... fees=0.001, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-6)... freq='1h'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-26-7)... )
 
[/code]

We've got a portfolio with two columns that can be analyzed with numerous built-in tools. For example, let's calculate and display the statistics for the `ETHUSDT` symbol:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-1)>>> pf['ETHUSDT'].stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-2)Start 2020-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-3)End 2021-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-4)Period 729 days 17:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-5)Start Value 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-6)Min Value 98.469385
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-7)Max Value 1805.987865
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-8)End Value 1135.272383
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-9)Total Return [%] 1035.272383
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-10)Benchmark Return [%] 2752.665477
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-11)Total Time Exposure [%] 51.750128
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-12)Max Gross Exposure [%] 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-13)Max Drawdown [%] 37.39953
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-14)Max Drawdown Duration 85 days 09:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-15)Total Orders 348
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-16)Total Fees Paid 272.755758
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-17)Total Trades 174
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-18)Win Rate [%] 43.103448
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-19)Best Trade [%] 33.286985
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-20)Worst Trade [%] -13.783496
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-21)Avg Winning Trade [%] 7.815551
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-22)Avg Losing Trade [%] -3.021041
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-23)Avg Winning Trade Duration 3 days 06:43:12
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-24)Avg Losing Trade Duration 1 days 07:54:32.727272727
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-25)Profit Factor 1.390947
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-26)Expectancy 5.949841
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-27)Sharpe Ratio 2.258501
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-28)Calmar Ratio 6.320363
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-29)Omega Ratio 1.103525
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-30)Sortino Ratio 3.27869
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-27-31)Name: ETHUSDT, dtype: object
 
[/code]


# Optimization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#optimization "Permanent link")

Optimization in vectorbt can be performed in two ways: iteratively and column-wise.

The first approach involves a simple loop that goes through every combination of the strategy's parameters and runs the whole logic. This would require you to manually generate a proper parameter grid and concatenate the results for analysis. On the upside, you would be able to use [Hyperopt](http://hyperopt.github.io/hyperopt/) and other tools that work on the per-iteration basis.

The second approach is natively supported by vectorbt and involves stacking columns. If you have 2 symbols and 5 parameters, vectorbt will generate 10 columns in total - one for each symbol and parameter, and backtest each column separately without leaving Numba (that's why most functions in vectorbt are specialized in processing two-dimensional data, by the way). Not only this has a huge performance benefit for small to medium-sized data, but this also enables parallelization with Numba and presentation of the results in a Pandas-friendly format.

Let's test the period values `4, 5, ..., 20`, and the multiplier values `2, 2.1, 2.2, ..., 4`, which would yield 336 parameter combinations in total. Since our indicator is now parametrized, we can pass those two parameter arrays directly to the `SuperTrend.run` method by also instructing it to do the [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product) using the `param_product=True` flag:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-1)>>> periods = np.arange(4, 20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-2)>>> multipliers = np.arange(20, 41) / 10 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-4)>>> st = SuperTrend.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-5)... high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-6)... period=periods, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-7)... multiplier=multipliers,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-8)... param_product=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-28-9)... )
 
[/code]

 1. 

Iteration 672/672

The indicator did 672 iterations - 336 per symbol. Let's see the columns that have been stacked:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-1)>>> st.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-2)MultiIndex([( 4, 2.0, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-3) ( 4, 2.0, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-4) ( 4, 2.1, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-5) ( 4, 2.1, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-6) ( 4, 2.2, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-7) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-8) (19, 3.8, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-9) (19, 3.9, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-10) (19, 3.9, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-11) (19, 4.0, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-12) (19, 4.0, 'ETHUSDT')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-29-13) names=['st_period', 'st_multiplier', 'symbol'], length=672)
 
[/code]

Each of the DataFrames has now 672 columns. Let's plot the latest combination by specifying the column as a regular tuple:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-30-1)>>> st.loc[date_range, (19, 4, 'ETHUSDT')].plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/optimization.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/optimization.dark.svg#only-dark)

When stacking a huge number of columns, make sure that you are not running out of RAM. You can print the size of any pickleable object in vectorbt using the [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize) method:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-31-1)>>> print(st.getsize())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-31-2)377.6 MB
 
[/code]

Which can be manually calculated as follows (without inputs and parameters):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-32-1)>>> output_size = st.wrapper.shape[0] * st.wrapper.shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-32-2)>>> n_outputs = 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-32-3)>>> data_type_size = 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-32-4)>>> input_size * n_outputs * data_type_size / 1024 / 1024
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-32-5)359.173828125
 
[/code]

Hint

To reduce the memory footprint, change the `get_final_bands_nb` function to produce the output arrays with a lesser floating point accuracy, such as `np.float32` or even `np.float16`.

The backtesting part remains the same, irrespective of the number of columns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-1)>>> entries = (~st.superl.isnull()).vbt.signals.fshift()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-2)>>> exits = (~st.supers.isnull()).vbt.signals.fshift()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-4)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-5)... close=close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-6)... entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-7)... exits=exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-8)... fees=0.001, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-9)... freq='1h'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-33-10)... )
 
[/code]

Instead of computing all the statistics for each single combination, let's plot a heatmap of their Sharpe values with the periods laid out horizontally and the multipliers laid out vertically. Since we have an additional column level that contains symbols, we'll make it a slider:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-34-1)>>> pf.sharpe_ratio.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-34-2)... x_level='st_period', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-34-3)... y_level='st_multiplier',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-34-4)... slider_level='symbol'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-34-5)... )
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/heatmap.dark.svg#only-dark)

We now have a nice overview of any parameter regions that performed well during the backtesting period, yay! ![🥳](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f973.svg)

Hint

To see how those Sharpe values perform against holding:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-35-1)>>> vbt.Portfolio.from_holding(close, freq='1h').sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-35-2)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-35-3)BTCUSDT 1.561447
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-35-4)ETHUSDT 2.170813
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/#__codelineno-35-5)Name: sharpe_ratio, dtype: float64
 
[/code]

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/superfast-supertrend/index.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SuperTrend.ipynb)